import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import * as fs from "fs/promises";
import * as path from "path";

type ContentBlock = {
    type?: string;
    text?: string;
    name?: string;
    arguments?: Record<string, unknown>;
};

type SessionEntry = {
    type: string;
    message?: {
        role?: string;
        content?: unknown;
    };
    timestamp?: number;
};

const extractTextParts = (content: unknown): string[] => {
    if (typeof content === "string") return [content];
    if (!Array.isArray(content)) return [];

    const textParts: string[] = [];
    for (const part of content) {
        if (!part || typeof part !== "object") continue;
        const block = part as ContentBlock;
        if (block.type === "text" && typeof block.text === "string") {
            textParts.push(block.text);
        }
    }
    return textParts;
};

const buildConversationText = (entries: SessionEntry[]): string => {
    const sections: string[] = [];

    for (const entry of entries) {
        if (entry.type !== "message" || !entry.message?.role) continue;
        
        const role = entry.message.role;
        const isUser = role === "user";
        const isAssistant = role === "assistant";

        if (!isUser && !isAssistant) continue;

        const entryLines: string[] = [];
        const textParts = extractTextParts(entry.message.content);
        if (textParts.length > 0) {
            const roleLabel = isUser ? "## User" : "## Assistant";
            const messageText = textParts.join("\n").trim();
            if (messageText.length > 0) {
                entryLines.push(`${roleLabel}\n\n${messageText}`);
            }
        }

        if (entryLines.length > 0) {
            sections.push(entryLines.join("\n"));
        }
    }

    return sections.join("\n\n---\n\n");
};

export default function (pi: ExtensionAPI) {
    pi.on("session_shutdown", async (_event, ctx) => {
        try {
            const branch = ctx.sessionManager.getBranch();
            const conversationText = buildConversationText(branch);
            
            if (!conversationText.trim()) return; // Nothing to log

            // Get session name or use timestamp
            const sessionName = pi.getSessionName() || ctx.sessionManager.getSessionFile()?.split('/').pop()?.replace('.jsonl', '') || Date.now().toString();
            const dateStr = new Date().toISOString().split('T')[0];
            const fileName = `${dateStr}-${sessionName}.md`.replace(/[^a-zA-Z0-9-_\.]/g, '_');
            
            const logDir = path.join(ctx.cwd, "agent", "conversations");
            await fs.mkdir(logDir, { recursive: true });
            
            const logPath = path.join(logDir, fileName);
            
            const fileContent = `# Conversation Log: ${sessionName}\n\n*Date: ${new Date().toISOString()}*\n\n---\n\n${conversationText}\n`;
            
            await fs.writeFile(logPath, fileContent, "utf-8");
            
            if (ctx.hasUI) {
                ctx.ui.notify(`Conversation logged to agent/conversations/${fileName}`, "info");
            }
        } catch (error) {
            if (ctx.hasUI) {
                ctx.ui.notify(`Failed to log conversation: ${error}`, "error");
            }
            console.error("Failed to log conversation:", error);
        }
    });
}
