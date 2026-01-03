// MyOS Desktop - Full Featured Version

let zIndex = 100;
let windows = [];
let activeWindow = null;
let openApps = new Set();

const apps = [
    { id: 'files', icon: '📁', name: 'Files' },
    { id: 'notepad', icon: '📝', name: 'Notepad' },
    { id: 'terminal', icon: '🖥️', name: 'Terminal' },
    { id: 'settings', icon: '⚙️', name: 'Settings' },
    { id: 'paint', icon: '🎨', name: 'Paint' },
    { id: 'calc', icon: '🧮', name: 'Calculator' },
    { id: 'browser', icon: '🌐', name: 'Browser' },
    { id: 'photos', icon: '🖼️', name: 'Photos' },
    { id: 'music', icon: '🎵', name: 'Music' },
    { id: 'games', icon: '🎮', name: 'Games' },
    { id: 'store', icon: '🛒', name: 'Store' },
    { id: 'about', icon: 'ℹ️', name: 'About' },
];

const desktopIcons = [
    { icon: '💻', label: 'This PC', app: 'files' },
    { icon: '📁', label: 'Documents', app: 'files' },
    { icon: '🗑️', label: 'Recycle Bin', app: null },
    { icon: '⚙️', label: 'Settings', app: 'settings' },
    { icon: '📝', label: 'Notepad', app: 'notepad' },
    { icon: '🎨', label: 'Paint', app: 'paint' },
];

function init() {
    createDesktopIcons();
    createTaskbar();
    createStartMenu();
    createContextMenu();
    updateClock();
    setInterval(updateClock, 1000);
    
    document.getElementById('desktop').onclick = (e) => {
        if (e.target.id === 'desktop') {
            closeStartMenu();
            hideContextMenu();
        }
    };
    
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeStartMenu();
        if (e.key === 'Meta' || (e.ctrlKey && e.key === 'Escape')) toggleStartMenu();
    });
}

function createDesktopIcons() {
    const desktop = document.getElementById('desktop');
    desktopIcons.forEach((item, i) => {
        const icon = document.createElement('div');
        icon.className = 'desktop-icon';
        icon.style.left = '20px';
        icon.style.top = (20 + i * 95) + 'px';
        icon.innerHTML = `<div class="icon">${item.icon}</div><div class="label">${item.label}</div>`;
        icon.ondblclick = () => item.app && openApp(item.app);
        desktop.appendChild(icon);
    });
}

function createTaskbar() {
    const taskbar = document.getElementById('taskbar');
    const mainApps = ['files', 'browser', 'notepad', 'terminal', 'settings'];
    
    // Start button
    const startBtn = document.createElement('button');
    startBtn.className = 'taskbar-btn';
    startBtn.innerHTML = '⊞';
    startBtn.onclick = toggleStartMenu;
    taskbar.appendChild(startBtn);
    
    // Search
    const searchBtn = document.createElement('button');
    searchBtn.className = 'taskbar-btn';
    searchBtn.innerHTML = '🔍';
    searchBtn.onclick = () => { toggleStartMenu(); document.querySelector('.start-search').focus(); };
    taskbar.appendChild(searchBtn);
    
    // App buttons
    mainApps.forEach(appId => {
        const app = apps.find(a => a.id === appId);
        const btn = document.createElement('button');
        btn.className = 'taskbar-btn';
        btn.id = 'taskbar-' + appId;
        btn.innerHTML = app.icon;
        btn.onclick = () => openApp(appId);
        taskbar.appendChild(btn);
    });
}

function createStartMenu() {
    const pinned = document.getElementById('pinned-apps');
    apps.forEach(app => {
        const btn = document.createElement('button');
        btn.className = 'app-btn';
        btn.innerHTML = `<span class="icon">${app.icon}</span><span class="label">${app.name}</span>`;
        btn.onclick = () => { openApp(app.id); closeStartMenu(); };
        pinned.appendChild(btn);
    });
}

function toggleStartMenu() {
    document.getElementById('start-menu').classList.toggle('open');
}

function closeStartMenu() {
    document.getElementById('start-menu').classList.remove('open');
}

function updateClock() {
    const now = new Date();
    document.getElementById('clock').innerHTML = 
        now.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' }) + '<br>' +
        now.toLocaleDateString('ru-RU', { day: '2-digit', month: '2-digit', year: 'numeric' });
}

// Context Menu
function createContextMenu() {
    document.getElementById('desktop').oncontextmenu = (e) => {
        e.preventDefault();
        showContextMenu(e.clientX, e.clientY, [
            { icon: '🔄', label: 'Refresh', action: () => location.reload() },
            { divider: true },
            { icon: '📁', label: 'New Folder', action: () => alert('Folder created!') },
            { icon: '📄', label: 'New File', action: () => openApp('notepad') },
            { divider: true },
            { icon: '🖼️', label: 'Change Wallpaper', action: changeWallpaper },
            { icon: '⚙️', label: 'Settings', action: () => openApp('settings') },
        ]);
    };
}

function showContextMenu(x, y, items) {
    const menu = document.getElementById('context-menu');
    menu.innerHTML = '';
    items.forEach(item => {
        if (item.divider) {
            menu.innerHTML += '<div class="ctx-divider"></div>';
        } else {
            const el = document.createElement('div');
            el.className = 'ctx-item';
            el.innerHTML = `<span>${item.icon}</span><span>${item.label}</span>`;
            el.onclick = () => { item.action(); hideContextMenu(); };
            menu.appendChild(el);
        }
    });
    menu.style.left = Math.min(x, window.innerWidth - 220) + 'px';
    menu.style.top = Math.min(y, window.innerHeight - menu.offsetHeight - 60) + 'px';
    menu.style.display = 'block';
}

function hideContextMenu() {
    document.getElementById('context-menu').style.display = 'none';
}

document.onclick = (e) => {
    if (!e.target.closest('#context-menu')) hideContextMenu();
};

let wallpaperIndex = 0;
const wallpapers = [
    'linear-gradient(135deg, #0078d4 0%, #001f54 50%, #1a0033 100%)',
    'linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)',
    'linear-gradient(135deg, #2d1b69 0%, #11998e 100%)',
    'linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%)',
    'linear-gradient(135deg, #000428 0%, #004e92 100%)',
];

function changeWallpaper() {
    wallpaperIndex = (wallpaperIndex + 1) % wallpapers.length;
    document.getElementById('desktop').style.background = wallpapers[wallpaperIndex];
}


// Window System
function createWindow(id, title, width, height, content) {
    closeStartMenu();
    
    // Check if already open
    const existing = document.querySelector(`.window[data-app="${id}"]`);
    if (existing) {
        focusWindow(existing);
        return existing;
    }
    
    const win = document.createElement('div');
    win.className = 'window';
    win.dataset.app = id;
    win.style.width = width + 'px';
    win.style.left = (100 + (windows.length % 5) * 40) + 'px';
    win.style.top = (60 + (windows.length % 5) * 40) + 'px';
    win.style.zIndex = ++zIndex;
    
    win.innerHTML = `
        <div class="window-titlebar">
            <span class="window-title">${title}</span>
            <div class="window-controls">
                <button class="win-ctrl minimize">─</button>
                <button class="win-ctrl maximize">□</button>
                <button class="win-ctrl close">✕</button>
            </div>
        </div>
        <div class="window-content" style="height:${height - 36}px">${content}</div>
    `;
    
    // Controls
    win.querySelector('.close').onclick = () => closeWindow(win);
    win.querySelector('.minimize').onclick = () => minimizeWindow(win);
    win.querySelector('.maximize').onclick = () => maximizeWindow(win);
    
    // Dragging
    makeDraggable(win, win.querySelector('.window-titlebar'));
    
    // Focus
    win.onmousedown = () => focusWindow(win);
    
    document.getElementById('desktop').appendChild(win);
    windows.push(win);
    openApps.add(id);
    updateTaskbarBtn(id, true);
    focusWindow(win);
    
    return win;
}

function focusWindow(win) {
    if (activeWindow) activeWindow.classList.remove('focused');
    win.classList.add('focused');
    win.style.zIndex = ++zIndex;
    activeWindow = win;
}

function closeWindow(win) {
    const id = win.dataset.app;
    win.style.opacity = '0';
    win.style.transform = 'scale(0.9)';
    setTimeout(() => {
        win.remove();
        windows = windows.filter(w => w !== win);
        openApps.delete(id);
        updateTaskbarBtn(id, false);
    }, 150);
}

function minimizeWindow(win) {
    win.style.display = 'none';
}

function maximizeWindow(win) {
    if (win.dataset.maximized === 'true') {
        win.style.left = win.dataset.oldLeft;
        win.style.top = win.dataset.oldTop;
        win.style.width = win.dataset.oldWidth;
        win.style.height = '';
        win.dataset.maximized = 'false';
    } else {
        win.dataset.oldLeft = win.style.left;
        win.dataset.oldTop = win.style.top;
        win.dataset.oldWidth = win.style.width;
        win.style.left = '0';
        win.style.top = '0';
        win.style.width = '100vw';
        win.style.height = 'calc(100vh - 52px)';
        win.querySelector('.window-content').style.height = 'calc(100vh - 88px)';
        win.dataset.maximized = 'true';
    }
}

function updateTaskbarBtn(id, active) {
    const btn = document.getElementById('taskbar-' + id);
    if (btn) btn.classList.toggle('active', active);
}

function makeDraggable(el, handle) {
    let startX, startY, startLeft, startTop;
    
    handle.onmousedown = (e) => {
        if (e.target.closest('.window-controls')) return;
        e.preventDefault();
        startX = e.clientX;
        startY = e.clientY;
        startLeft = el.offsetLeft;
        startTop = el.offsetTop;
        el.style.zIndex = ++zIndex;
        
        const move = (e) => {
            el.style.left = (startLeft + e.clientX - startX) + 'px';
            el.style.top = Math.max(0, startTop + e.clientY - startY) + 'px';
        };
        
        const up = () => {
            document.removeEventListener('mousemove', move);
            document.removeEventListener('mouseup', up);
        };
        
        document.addEventListener('mousemove', move);
        document.addEventListener('mouseup', up);
    };
}

// Apps
function openApp(id) {
    const existing = document.querySelector(`.window[data-app="${id}"]`);
    if (existing) {
        existing.style.display = 'block';
        focusWindow(existing);
        return;
    }
    
    const appContent = getAppContent(id);
    createWindow(id, appContent.title, appContent.width, appContent.height, appContent.html);
    
    // Post-init
    if (appContent.init) setTimeout(appContent.init, 50);
}

function getAppContent(id) {
    switch(id) {
        case 'files':
            return {
                title: '📁 File Explorer',
                width: 600, height: 450,
                html: `
                    <div style="display:flex;height:100%">
                        <div style="width:180px;background:#252525;padding:12px;border-right:1px solid #333">
                            <div style="color:#888;font-size:11px;margin-bottom:8px">Quick Access</div>
                            ${['📁 Desktop', '📁 Downloads', '📁 Documents', '📁 Pictures', '📁 Music'].map(f => 
                                `<div style="color:white;padding:8px;border-radius:6px;cursor:pointer;margin:2px 0" onmouseover="this.style.background='#333'" onmouseout="this.style.background=''">${f}</div>`
                            ).join('')}
                            <div style="color:#888;font-size:11px;margin:16px 0 8px">This PC</div>
                            ${['💾 Local Disk (C:)', '💿 DVD Drive (D:)'].map(f => 
                                `<div style="color:white;padding:8px;border-radius:6px;cursor:pointer;margin:2px 0" onmouseover="this.style.background='#333'" onmouseout="this.style.background=''">${f}</div>`
                            ).join('')}
                        </div>
                        <div style="flex:1;padding:16px">
                            <div style="color:white;font-size:18px;margin-bottom:16px">📁 This PC</div>
                            <div style="display:grid;grid-template-columns:repeat(auto-fill,100px);gap:12px">
                                ${['📁 Desktop', '📁 Documents', '📁 Downloads', '📁 Pictures', '📁 Music', '📁 Videos'].map(f => 
                                    `<div style="text-align:center;padding:12px;border-radius:8px;cursor:pointer;transition:all 0.15s" onmouseover="this.style.background='#333'" onmouseout="this.style.background=''">
                                        <div style="font-size:36px">${f.split(' ')[0]}</div>
                                        <div style="color:white;font-size:12px;margin-top:6px">${f.split(' ')[1]}</div>
                                    </div>`
                                ).join('')}
                            </div>
                        </div>
                    </div>`
            };
            
        case 'notepad':
            return {
                title: '📝 Notepad',
                width: 550, height: 420,
                html: `
                    <div style="display:flex;flex-direction:column;height:100%">
                        <div style="background:#2a2a2a;padding:4px 8px;display:flex;gap:16px;font-size:13px;color:#ccc;border-bottom:1px solid #333">
                            <span style="cursor:pointer" onmouseover="this.style.color='white'" onmouseout="this.style.color='#ccc'">File</span>
                            <span style="cursor:pointer" onmouseover="this.style.color='white'" onmouseout="this.style.color='#ccc'">Edit</span>
                            <span style="cursor:pointer" onmouseover="this.style.color='white'" onmouseout="this.style.color='#ccc'">View</span>
                        </div>
                        <textarea id="notepad-text" style="flex:1;background:#1e1e1e;color:#d4d4d4;border:none;padding:12px;font-family:'Cascadia Code',Consolas,monospace;font-size:14px;resize:none;line-height:1.5" placeholder="Start typing..."></textarea>
                        <div style="background:#2a2a2a;padding:4px 12px;font-size:11px;color:#888;display:flex;justify-content:space-between">
                            <span id="notepad-status">Ln 1, Col 1</span>
                            <span>UTF-8</span>
                        </div>
                    </div>`,
                init: () => {
                    const ta = document.getElementById('notepad-text');
                    const status = document.getElementById('notepad-status');
                    ta.oninput = ta.onclick = ta.onkeyup = () => {
                        const lines = ta.value.substr(0, ta.selectionStart).split('\n');
                        status.textContent = `Ln ${lines.length}, Col ${lines[lines.length-1].length + 1}`;
                    };
                }
            };
            
        case 'terminal':
            return {
                title: '🖥️ Terminal',
                width: 650, height: 420,
                html: `
                    <div id="terminal" style="background:#0c0c0c;height:100%;padding:12px;font-family:'Cascadia Code',Consolas,monospace;font-size:13px;overflow-y:auto">
                        <div style="color:#3b78ff">MyOS Terminal v1.0</div>
                        <div style="color:#666">Type 'help' for commands</div>
                        <br>
                        <div id="term-output"></div>
                        <div style="display:flex;color:#16c60c">
                            <span>C:\\Users\\User&gt;&nbsp;</span>
                            <input id="term-input" style="flex:1;background:transparent;border:none;color:#cccccc;font-family:inherit;font-size:inherit;outline:none" autofocus>
                        </div>
                    </div>`,
                init: () => {
                    const input = document.getElementById('term-input');
                    const output = document.getElementById('term-output');
                    const commands = {
                        help: 'Available commands: help, clear, date, echo, whoami, ls, cat, neofetch',
                        clear: () => { output.innerHTML = ''; return ''; },
                        date: new Date().toString(),
                        whoami: 'User',
                        ls: 'Desktop  Documents  Downloads  Pictures  Music  Videos',
                        neofetch: `<pre style="color:#3b78ff">
  ███╗   ███╗██╗   ██╗ ██████╗ ███████╗
  ████╗ ████║╚██╗ ██╔╝██╔═══██╗██╔════╝
  ██╔████╔██║ ╚████╔╝ ██║   ██║███████╗
  ██║╚██╔╝██║  ╚██╔╝  ██║   ██║╚════██║
  ██║ ╚═╝ ██║   ██║   ╚██████╔╝███████║
  ╚═╝     ╚═╝   ╚═╝    ╚═════╝ ╚══════╝</pre>
  <span style="color:#ccc">OS:</span> MyOS 1.0
  <span style="color:#ccc">Kernel:</span> Web 1.0
  <span style="color:#ccc">Shell:</span> mysh
  <span style="color:#ccc">Resolution:</span> ${window.innerWidth}x${window.innerHeight}`,
                    };
                    
                    input.onkeydown = (e) => {
                        if (e.key === 'Enter') {
                            const cmd = input.value.trim();
                            const parts = cmd.split(' ');
                            let result = '';
                            
                            if (cmd === '') result = '';
                            else if (parts[0] === 'echo') result = parts.slice(1).join(' ');
                            else if (parts[0] === 'cat') result = 'File not found: ' + (parts[1] || '');
                            else if (commands[cmd]) result = typeof commands[cmd] === 'function' ? commands[cmd]() : commands[cmd];
                            else result = `'${cmd}' is not recognized as a command`;
                            
                            output.innerHTML += `<div style="color:#16c60c">C:\\Users\\User&gt; <span style="color:#ccc">${cmd}</span></div>`;
                            if (result) output.innerHTML += `<div style="color:#ccc;margin-bottom:8px">${result}</div>`;
                            input.value = '';
                            document.getElementById('terminal').scrollTop = 99999;
                        }
                    };
                }
            };
            
        case 'settings':
            return {
                title: '⚙️ Settings',
                width: 700, height: 500,
                html: `
                    <div style="display:flex;height:100%">
                        <div style="width:200px;background:#202020;padding:16px">
                            ${['🏠 Home', '💻 System', '📱 Devices', '📶 Network', '🎨 Personalization', '🔒 Privacy', '🔄 Update'].map((item, i) => 
                                `<div style="color:${i===0?'white':'#aaa'};padding:10px 12px;border-radius:6px;cursor:pointer;margin:2px 0;background:${i===0?'#0078d4':''}" 
                                    onmouseover="if(!this.style.background.includes('0078d4'))this.style.background='#333'" 
                                    onmouseout="if(!this.style.background.includes('0078d4'))this.style.background=''">${item}</div>`
                            ).join('')}
                        </div>
                        <div style="flex:1;padding:24px;overflow-y:auto">
                            <h2 style="color:white;font-weight:500;margin-bottom:24px">Settings</h2>
                            <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:12px">
                                ${[
                                    ['💻', 'System', 'Display, sound, notifications'],
                                    ['📱', 'Devices', 'Bluetooth, printers, mouse'],
                                    ['📶', 'Network', 'Wi-Fi, VPN, proxy'],
                                    ['🎨', 'Personalization', 'Background, colors, themes'],
                                    ['🔒', 'Privacy', 'Location, camera, microphone'],
                                    ['🔄', 'Update', 'Windows Update, recovery'],
                                ].map(([icon, title, desc]) => `
                                    <div style="background:#2a2a2a;padding:16px;border-radius:8px;cursor:pointer;transition:all 0.15s" 
                                        onmouseover="this.style.background='#333'" onmouseout="this.style.background='#2a2a2a'">
                                        <div style="font-size:28px;margin-bottom:8px">${icon}</div>
                                        <div style="color:white;font-size:14px;font-weight:500">${title}</div>
                                        <div style="color:#888;font-size:12px;margin-top:4px">${desc}</div>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    </div>`
            };

            
        case 'paint':
            return {
                title: '🎨 Paint',
                width: 700, height: 500,
                html: `
                    <div style="display:flex;flex-direction:column;height:100%">
                        <div style="background:#2a2a2a;padding:8px;display:flex;gap:8px;align-items:center;border-bottom:1px solid #333">
                            <div style="display:flex;gap:4px">
                                ${['#000000','#ffffff','#ff0000','#00ff00','#0000ff','#ffff00','#ff00ff','#00ffff','#ff8800','#8800ff'].map(c => 
                                    `<div class="color-btn" data-color="${c}" style="width:24px;height:24px;background:${c};border-radius:4px;cursor:pointer;border:2px solid ${c==='#000000'?'#0078d4':'transparent'}" onclick="selectColor('${c}',this)"></div>`
                                ).join('')}
                            </div>
                            <div style="width:1px;height:24px;background:#444;margin:0 8px"></div>
                            <div style="display:flex;gap:4px">
                                ${[2,5,10,20].map(s => 
                                    `<div class="size-btn" data-size="${s}" style="width:28px;height:28px;background:#333;border-radius:4px;cursor:pointer;display:flex;align-items:center;justify-content:center;border:2px solid ${s===5?'#0078d4':'transparent'}" onclick="selectSize(${s},this)">
                                        <div style="width:${Math.min(s,16)}px;height:${Math.min(s,16)}px;background:white;border-radius:50%"></div>
                                    </div>`
                                ).join('')}
                            </div>
                            <div style="width:1px;height:24px;background:#444;margin:0 8px"></div>
                            <button onclick="clearCanvas()" style="background:#333;border:none;color:white;padding:6px 12px;border-radius:4px;cursor:pointer">Clear</button>
                            <button onclick="saveCanvas()" style="background:#0078d4;border:none;color:white;padding:6px 12px;border-radius:4px;cursor:pointer">Save</button>
                        </div>
                        <canvas id="paint-canvas" style="flex:1;background:white;cursor:crosshair"></canvas>
                    </div>`,
                init: () => {
                    const canvas = document.getElementById('paint-canvas');
                    const ctx = canvas.getContext('2d');
                    canvas.width = 696;
                    canvas.height = 420;
                    
                    window.paintColor = '#000000';
                    window.paintSize = 5;
                    let drawing = false;
                    let lastX, lastY;
                    
                    canvas.onmousedown = (e) => {
                        drawing = true;
                        [lastX, lastY] = [e.offsetX, e.offsetY];
                    };
                    canvas.onmouseup = () => drawing = false;
                    canvas.onmouseleave = () => drawing = false;
                    canvas.onmousemove = (e) => {
                        if (!drawing) return;
                        ctx.beginPath();
                        ctx.strokeStyle = window.paintColor;
                        ctx.lineWidth = window.paintSize;
                        ctx.lineCap = 'round';
                        ctx.moveTo(lastX, lastY);
                        ctx.lineTo(e.offsetX, e.offsetY);
                        ctx.stroke();
                        [lastX, lastY] = [e.offsetX, e.offsetY];
                    };
                    
                    window.selectColor = (c, el) => {
                        window.paintColor = c;
                        document.querySelectorAll('.color-btn').forEach(b => b.style.borderColor = 'transparent');
                        el.style.borderColor = '#0078d4';
                    };
                    window.selectSize = (s, el) => {
                        window.paintSize = s;
                        document.querySelectorAll('.size-btn').forEach(b => b.style.borderColor = 'transparent');
                        el.style.borderColor = '#0078d4';
                    };
                    window.clearCanvas = () => ctx.clearRect(0, 0, canvas.width, canvas.height);
                    window.saveCanvas = () => {
                        const link = document.createElement('a');
                        link.download = 'drawing.png';
                        link.href = canvas.toDataURL();
                        link.click();
                    };
                }
            };
            
        case 'calc':
            return {
                title: '🧮 Calculator',
                width: 280, height: 420,
                html: `
                    <div style="padding:12px;height:100%;display:flex;flex-direction:column">
                        <input type="text" id="calc-display" value="0" readonly style="width:100%;padding:16px;font-size:32px;text-align:right;background:#1a1a1a;color:white;border:none;border-radius:8px;margin-bottom:12px;font-family:'Segoe UI'">
                        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:6px;flex:1">
                            ${['C','±','%','÷','7','8','9','×','4','5','6','-','1','2','3','+'].map(b => 
                                `<button onclick="calcBtn('${b}')" style="background:${['÷','×','-','+'].includes(b)?'#505050':'C±%'.includes(b)?'#333':'#3d3d3d'};border:none;color:white;font-size:18px;border-radius:8px;cursor:pointer;transition:all 0.1s" onmouseover="this.style.opacity='0.8'" onmouseout="this.style.opacity='1'">${b}</button>`
                            ).join('')}
                            <button onclick="calcBtn('0')" style="grid-column:span 2;background:#3d3d3d;border:none;color:white;font-size:18px;border-radius:8px;cursor:pointer" onmouseover="this.style.opacity='0.8'" onmouseout="this.style.opacity='1'">0</button>
                            <button onclick="calcBtn('.')" style="background:#3d3d3d;border:none;color:white;font-size:18px;border-radius:8px;cursor:pointer" onmouseover="this.style.opacity='0.8'" onmouseout="this.style.opacity='1'">.</button>
                            <button onclick="calcBtn('=')" style="background:#0078d4;border:none;color:white;font-size:18px;border-radius:8px;cursor:pointer" onmouseover="this.style.opacity='0.8'" onmouseout="this.style.opacity='1'">=</button>
                        </div>
                    </div>`,
                init: () => {
                    window.calcValue = '0';
                    window.calcBtn = (v) => {
                        const display = document.getElementById('calc-display');
                        if (v === 'C') window.calcValue = '0';
                        else if (v === '±') window.calcValue = String(-parseFloat(window.calcValue));
                        else if (v === '%') window.calcValue = String(parseFloat(window.calcValue) / 100);
                        else if (v === '=') {
                            try {
                                window.calcValue = String(eval(window.calcValue.replace(/×/g,'*').replace(/÷/g,'/')));
                            } catch { window.calcValue = 'Error'; }
                        }
                        else if ('÷×-+'.includes(v)) window.calcValue += v;
                        else {
                            if (window.calcValue === '0' && v !== '.') window.calcValue = v;
                            else window.calcValue += v;
                        }
                        display.value = window.calcValue;
                    };
                }
            };
            
        case 'browser':
            return {
                title: '🌐 Browser',
                width: 800, height: 550,
                html: `
                    <div style="display:flex;flex-direction:column;height:100%">
                        <div style="background:#2a2a2a;padding:8px;display:flex;gap:8px;align-items:center">
                            <button style="background:#333;border:none;color:white;width:32px;height:32px;border-radius:6px;cursor:pointer">←</button>
                            <button style="background:#333;border:none;color:white;width:32px;height:32px;border-radius:6px;cursor:pointer">→</button>
                            <button style="background:#333;border:none;color:white;width:32px;height:32px;border-radius:6px;cursor:pointer">🔄</button>
                            <input id="browser-url" type="text" value="https://myos.local" style="flex:1;padding:8px 12px;background:#1a1a1a;border:1px solid #333;color:white;border-radius:6px;font-size:13px">
                            <button onclick="browserGo()" style="background:#0078d4;border:none;color:white;padding:8px 16px;border-radius:6px;cursor:pointer">Go</button>
                        </div>
                        <div id="browser-content" style="flex:1;background:#1a1a1a;display:flex;align-items:center;justify-content:center;flex-direction:column;color:#888">
                            <div style="font-size:64px;margin-bottom:16px">🌐</div>
                            <h2 style="color:white;margin-bottom:8px">Welcome to MyOS Browser</h2>
                            <p>Enter a URL or search the web</p>
                        </div>
                    </div>`,
                init: () => {
                    window.browserGo = () => {
                        const url = document.getElementById('browser-url').value;
                        const content = document.getElementById('browser-content');
                        content.innerHTML = `<div style="font-size:48px;margin-bottom:16px">🔒</div><h3 style="color:white">Cannot connect to ${url}</h3><p style="color:#888">This is a demo browser</p>`;
                    };
                    document.getElementById('browser-url').onkeydown = (e) => { if (e.key === 'Enter') window.browserGo(); };
                }
            };
            
        case 'about':
            return {
                title: 'ℹ️ About MyOS',
                width: 450, height: 350,
                html: `
                    <div style="padding:32px;text-align:center;color:white">
                        <div style="font-size:72px;margin-bottom:16px">💻</div>
                        <h1 style="font-weight:500;margin-bottom:8px">MyOS</h1>
                        <p style="color:#888;margin-bottom:24px">Version 1.0.0</p>
                        <div style="background:#2a2a2a;padding:16px;border-radius:8px;text-align:left;font-size:13px;color:#aaa">
                            <p style="margin-bottom:8px"><strong style="color:white">OS:</strong> MyOS Desktop</p>
                            <p style="margin-bottom:8px"><strong style="color:white">Kernel:</strong> Web 1.0</p>
                            <p style="margin-bottom:8px"><strong style="color:white">Resolution:</strong> ${window.innerWidth}×${window.innerHeight}</p>
                            <p><strong style="color:white">Memory:</strong> Unlimited</p>
                        </div>
                        <p style="color:#666;font-size:12px;margin-top:24px">© 2024 MyOS. All rights reserved.</p>
                    </div>`
            };
            
        default:
            return {
                title: apps.find(a => a.id === id)?.name || 'App',
                width: 400, height: 300,
                html: `<div style="display:flex;align-items:center;justify-content:center;height:100%;color:#888;flex-direction:column">
                    <div style="font-size:48px;margin-bottom:16px">${apps.find(a => a.id === id)?.icon || '📦'}</div>
                    <p>Coming soon!</p>
                </div>`
            };
    }
}

function shutdown() {
    document.body.style.transition = 'opacity 0.5s';
    document.body.style.opacity = '0';
    setTimeout(() => {
        document.body.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;height:100vh;background:#000;color:white;font-family:Segoe UI"><h1>Goodbye! 👋</h1></div>';
        document.body.style.opacity = '1';
    }, 500);
}

window.onload = init;
