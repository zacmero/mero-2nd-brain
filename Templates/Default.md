<%*
// 1. Gather all markdown files in the vault (excluding the index itself)
const files = app.vault.getMarkdownFiles().filter(f => f.path !== "vault_index.json");

// 2. Map the data into a clean, lightweight JSON structure
const indexData = [];
for (const file of files) {
    const cache = app.metadataCache.getFileCache(file);
    const fm = cache?.frontmatter || {};
    
    // Extract tags from cache or frontmatter
    let tags = [];
    if (cache?.tags) {
        tags = cache.tags.map(t => t.tag);
    } else if (fm.tags) {
        tags = fm.tags;
    }
    
    const aliases = fm.aliases || [];
    
    // Convert tags/aliases to array if they are strings
    const tagArray = Array.isArray(tags) ? tags : (typeof tags === 'string' ? [tags] : []);
    const aliasArray = Array.isArray(aliases) ? aliases : (typeof aliases === 'string' ? [aliases] : []);

    indexData.push({
        title: file.basename,
        path: file.path,
        tags: tagArray,
        summary: fm.summary || fm.description || (aliasArray.length > 0 ? aliasArray[0] : "")
    });
}

// 3. Write the JSON file directly to the root of your vault
const filePath = "vault_index.json";
const fileContent = JSON.stringify(indexData, null, 2);

const existingFile = app.vault.getAbstractFileByPath(filePath);
if (existingFile) {
    await app.vault.modify(existingFile, fileContent);
} else {
    await app.vault.create(filePath, fileContent);
}
%>