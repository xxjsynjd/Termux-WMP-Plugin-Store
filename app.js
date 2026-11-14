document.addEventListener('DOMContentLoaded', () => {
    let allPackages = [];

    fetch('Packages.json')
        .then(res => res.json())
        .then(data => {
            allPackages = data.packages || [];
            renderPlugins(allPackages);
        })
        .catch(err => {
            document.getElementById('pluginGrid').innerHTML = '<div class="loading">加载失败，请确认 Packages.json 是否存在。</div>';
            console.error('加载索引失败:', err);
        });

    document.getElementById('searchInput').addEventListener('input', (e) => {
        const keyword = e.target.value.toLowerCase();
        const filtered = allPackages.filter(p => 
            p.name.toLowerCase().includes(keyword) || 
            p.description.toLowerCase().includes(keyword)
        );
        renderPlugins(filtered);
    });
});

function renderPlugins(packages) {
    const grid = document.getElementById('pluginGrid');
    if (packages.length === 0) {
        grid.innerHTML = '<div class="loading">没有找到匹配的插件。</div>';
        return;
    }

    grid.innerHTML = packages.map(pkg => `
        <div class="card">
            <h2>${pkg.name}</h2>
            <span class="tag">${pkg.category}</span>
            <p class="desc">${pkg.description}</p>
            <div class="meta">
                <span>版本: v${pkg.version}</span> <br> <span>作者: ${pkg.author}</span>
            </div>
            <button class="btn-copy" onclick="copyInstallCmd('${pkg.name}')">
                复制安装命令
            </button>
        </div>
    `).join('');
}

function copyInstallCmd(pkgName) {
    const cmd = `twmpxpem install ${pkgName}`;
    navigator.clipboard.writeText(cmd).then(() => {
        alert(`已复制到剪贴板：\n${cmd}\n\n请在 Termux 中粘贴并回车运行。`);
    });
}
