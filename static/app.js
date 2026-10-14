/**
 * DEX CONTROL — Stream Deck Application Engine for iPad Safari & Desktop
 */

// SVG Icon Library
const ICONS = {
    'play': '<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>',
    'pause': '<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect></svg>',
    'skip-forward': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 4 15 12 5 20 5 4"></polygon><line x1="19" y1="5" x2="19" y2="19"></line></svg>',
    'skip-back': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="19 20 9 12 19 4 19 20"></polygon><line x1="5" y1="19" x2="5" y2="5"></line></svg>',
    'volume': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon></svg>',
    'volume-1': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path></svg>',
    'volume-2': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path></svg>',
    'volume-x': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><line x1="23" y1="9" x2="17" y2="15"></line><line x1="17" y1="9" x2="23" y2="15"></line></svg>',
    'camera': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path><circle cx="12" cy="13" r="4"></circle></svg>',
    'monitor': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>',
    'code': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 18 22 12 16 6"></polyline><polyline points="8 6 2 12 8 18"></polyline></svg>',
    'terminal': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="4 17 10 11 4 5"></polyline><line x1="12" y1="19" x2="20" y2="19"></line></svg>',
    'command-line': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 17l6-6-6-6M12 19h8"></path></svg>',
    'globe': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>',
    'folder': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>',
    'activity': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>',
    'settings': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>',
    'lock': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>',
    'sparkles': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3l1.9 5.8a2 2 0 0 0 1.3 1.3L21 12l-5.8 1.9a2 2 0 0 0-1.3 1.3L12 21l-1.9-5.8a2 2 0 0 0-1.3-1.3L3 12l5.8-1.9a2 2 0 0 0 1.3-1.3L12 3z"></path></svg>',
    'crop': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 2v14a2 2 0 0 0 2 2h14"></path><path d="M18 22V8a2 2 0 0 0-2-2H2"></path></svg>',
    'layers': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline></svg>',
    'rotate-ccw': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="1 4 1 10 7 10"></polyline><path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"></path></svg>',
    'corner-up-left': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 14 4 9 9 4"></polyline><path d="M20 20v-7a4 4 0 0 0-4-4H4"></path></svg>',
    'copy': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>',
    'clipboard': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg>',
    'message-circle': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path></svg>',
    'gamepad': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="6" y1="12" x2="10" y2="12"></line><line x1="8" y1="10" x2="8" y2="14"></line><line x1="15" y1="13" x2="15.01" y2="13"></line><line x1="18" y1="11" x2="18.01" y2="11"></line><rect x="2" y="6" width="20" height="12" rx="6"></rect></svg>',
    'music': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18V5l12-2v13"></path><circle cx="6" cy="18" r="3"></circle><circle cx="18" cy="16" r="3"></circle></svg>',
    'eye': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>',
    'layout-grid': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>'
};

// Global App State
const state = {
    csrfToken: window.DEX_CSRF || window.FURY_CSRF || '',
    activeProfileId: localStorage.getItem('dex_active_profile') || localStorage.getItem('fury_active_profile') || 'general',
    profilesData: null,
    appsData: [],
    macrosData: {},
    isEditingGrid: false,
    editingButtonIndex: null,
    isDraggingVolume: false,
    pollTimer: null,
    lastVolume: null
};

// ==================== CORE API CLIENT ====================
async function apiRequest(endpoint, method = 'GET', data = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRF-Token': state.csrfToken
        }
    };
    if (data && (method === 'POST' || method === 'PUT' || method === 'DELETE')) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const res = await fetch(endpoint, options);
        if (res.status === 401) {
            updateConnectionStatus('auth_required');
            window.location.href = '/login';
            return { ok: false, error: 'UNAUTHORIZED' };
        }
        const json = await res.json();
        if (json.csrf_token) {
            state.csrfToken = json.csrf_token;
        }
        return json;
    } catch (err) {
        updateConnectionStatus('disconnected');
        return { ok: false, error: 'NETWORK_ERROR', message: err.message };
    }
}

// ==================== TOAST NOTIFICATIONS ====================
function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `<span>${message}</span>`;
    container.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 250);
    }, 3200);
}

// ==================== CONNECTION STATUS ====================
function updateConnectionStatus(status) {
    const badge = document.getElementById('connectionStatus');
    const label = badge.querySelector('.status-label');
    badge.className = 'connection-badge';

    if (status === 'connected') {
        badge.classList.add('status-connected');
        label.textContent = 'Connected';
    } else if (status === 'connecting') {
        badge.classList.add('status-connecting');
        label.textContent = 'Connecting';
    } else if (status === 'auth_required') {
        badge.classList.add('status-disconnected');
        label.textContent = 'Auth Required';
    } else {
        badge.classList.add('status-disconnected');
        label.textContent = 'Disconnected';
    }
}

// ==================== HEARTBEAT & SYNC ====================
async function pollStatus() {
    const res = await apiRequest('/api/v1/status');
    if (res.ok) {
        updateConnectionStatus('connected');
        if (res.volume && !state.isDraggingVolume) {
            updateVolumeUI(res.volume.volume, res.volume.is_muted);
        }
        if (res.media) {
            updateNowPlayingUI(res.media);
        }
    }
}

function updateVolumeUI(volume, isMuted) {
    state.lastVolume = volume;
    const txt = isMuted ? 'Muted' : `${volume}%`;
    document.getElementById('homeVolumePercent').textContent = txt;
    document.getElementById('quickVolumeText').textContent = txt;
    document.getElementById('mediaMasterVolLabel').textContent = txt;

    const homeSlider = document.getElementById('homeVolumeSlider');
    const mediaSlider = document.getElementById('mediaVolumeSlider');
    if (!state.isDraggingVolume) {
        homeSlider.value = volume;
        mediaSlider.value = volume;
    }

    const muteIcon = document.getElementById('quickMuteIcon');
    if (isMuted) {
        muteIcon.innerHTML = ICONS['volume-x'];
    } else if (volume > 50) {
        muteIcon.innerHTML = ICONS['volume-2'];
    } else if (volume > 0) {
        muteIcon.innerHTML = ICONS['volume-1'];
    } else {
        muteIcon.innerHTML = ICONS['volume-x'];
    }
}

function updateNowPlayingUI(media) {
    const sourceTag = document.getElementById('mediaAppSource');
    const titleEl = document.getElementById('mediaTrackTitle');
    const artistEl = document.getElementById('mediaArtistAlbum');
    const stateBadge = document.getElementById('mediaStateBadge');
    const heroBtn = document.getElementById('mediaPlayPauseBtn');
    const progWrap = document.getElementById('mediaProgressContainer');

    if (media.has_session && media.title) {
        sourceTag.textContent = media.app_id || 'Active Player';
        titleEl.textContent = media.title;
        artistEl.textContent = [media.artist, media.album].filter(Boolean).join(' • ') || 'Media Playing';
        stateBadge.textContent = media.playback_status || 'Playing';
        stateBadge.className = 'badge-status status-ready';

        if (media.playback_status === 'Playing') {
            heroBtn.innerHTML = ICONS['pause'];
        } else {
            heroBtn.innerHTML = ICONS['play'];
        }

        if (media.duration > 0) {
            progWrap.style.display = 'flex';
            const pos = media.position || 0;
            const dur = media.duration;
            const pct = Math.min(100, Math.max(0, (pos / dur) * 100));
            document.getElementById('mediaProgressFill').style.width = `${pct}%`;
            document.getElementById('mediaTimeElapsed').textContent = formatSeconds(pos);
            document.getElementById('mediaTimeTotal').textContent = formatSeconds(dur);
        } else {
            progWrap.style.display = 'none';
        }
    } else {
        sourceTag.textContent = 'No Active Session';
        titleEl.textContent = 'Playback Idle';
        artistEl.textContent = 'Start playing media in Chrome, Spotify, or YouTube';
        stateBadge.textContent = 'Idle';
        stateBadge.className = 'badge-status status-idle';
        heroBtn.innerHTML = ICONS['play'];
        progWrap.style.display = 'none';
    }
}

function formatSeconds(secs) {
    const s = Math.floor(secs);
    const m = Math.floor(s / 60);
    const r = s % 60;
    return `${m}:${r < 10 ? '0' : ''}${r}`;
}

// ==================== ACTION DISPATCHER ====================
async function executeAction(actionName, params = {}, btnEl = null) {
    if (btnEl) {
        btnEl.classList.remove('is-success', 'is-error');
        btnEl.classList.add('is-executing');
    }

    const res = await apiRequest('/api/v1/actions', 'POST', {
        action: actionName,
        params: params
    });

    if (btnEl) {
        btnEl.classList.remove('is-executing');
        if (res.ok) {
            btnEl.classList.add('is-success');
            setTimeout(() => btnEl.classList.remove('is-success'), 900);
        } else {
            btnEl.classList.add('is-error');
            setTimeout(() => btnEl.classList.remove('is-error'), 1200);
        }
    }

    if (res.ok) {
        showToast(res.message || 'Action executed', 'success');
        refreshHistory();
        // Immediately sync volume if volume action
        if (actionName.includes('volume') || actionName.includes('mute')) {
            if (res.result && typeof res.result.volume === 'number') {
                updateVolumeUI(res.result.volume, res.result.is_muted);
            } else {
                pollStatus();
            }
        }
    } else {
        showToast(res.message || res.error || 'Action failed', 'error');
    }
    return res;
}

// ==================== ACTIVITY FEED ====================
async function refreshHistory() {
    const res = await apiRequest('/api/v1/history');
    if (!res.ok || !res.history) return;

    const feed = document.getElementById('activityFeed');
    if (res.history.length === 0) {
        feed.innerHTML = '<div class="feed-empty">No actions executed yet. Tap any key on your iPad!</div>';
        return;
    }

    feed.innerHTML = res.history.map(item => `
        <div class="feed-item">
            <div class="feed-item-left">
                <span class="status-dot" style="background: ${item.success ? 'var(--success)' : 'var(--danger)'}"></span>
                <span class="feed-item-action">${escapeHtml(item.action)}</span>
                <span class="feed-item-details">${escapeHtml(item.details)}</span>
            </div>
            <span class="feed-item-time">${item.time_str || ''}</span>
        </div>
    `).join('');
}

// ==================== STREAM DECK GRID RENDERING ====================
async function loadProfiles() {
    const res = await apiRequest('/api/v1/profiles');
    if (res && res.profiles) {
        state.profilesData = res;
        renderHeaderProfileSelect();
        renderActiveDeckGrid();
        renderProfilesManager();
    }
}

function renderHeaderProfileSelect() {
    const select = document.getElementById('headerProfileSelect');
    if (!state.profilesData) return;

    select.innerHTML = Object.keys(state.profilesData.profiles).map(id => {
        const p = state.profilesData.profiles[id];
        return `<option value="${id}" ${id === state.activeProfileId ? 'selected' : ''}>${escapeHtml(p.name)}</option>`;
    }).join('');
}

function renderActiveDeckGrid() {
    if (!state.profilesData) return;
    const profile = state.profilesData.profiles[state.activeProfileId];
    if (!profile) return;

    document.getElementById('activeProfileTitle').textContent = `${profile.name} Deck`;
    document.getElementById('activeProfileDesc').textContent = profile.description || 'Touch keys';

    const grid = document.getElementById('deckGrid');
    const buttons = profile.buttons || [];

    grid.innerHTML = buttons.map((btn, idx) => {
        const iconSvg = ICONS[btn.icon] || ICONS['sparkles'];
        const sizeClass = btn.size === '2x1' ? 'size-2x1' : '';
        const editBar = state.isEditingGrid ? `
            <div class="key-edit-bar">
                <span class="key-edit-icon" onclick="event.stopPropagation(); moveButton(${idx}, -1)" title="Move Left/Up">◀</span>
                <span class="key-edit-icon" onclick="event.stopPropagation(); moveButton(${idx}, 1)" title="Move Right/Down">▶</span>
                <span class="key-edit-icon" onclick="event.stopPropagation(); openEditButtonModal(${idx})" title="Edit">✎</span>
            </div>
        ` : '';

        return `
            <div class="deck-key ${sizeClass}" id="btnKey_${idx}" onclick="handleDeckKeyClick(${idx}, this)">
                ${editBar}
                <div class="deck-key-icon">${iconSvg}</div>
                <div class="deck-key-label">${escapeHtml(btn.label)}</div>
            </div>
        `;
    }).join('');

    if (state.isEditingGrid) {
        const addBtn = document.createElement('div');
        addBtn.className = 'deck-key';
        addBtn.style.borderStyle = 'dashed';
        addBtn.innerHTML = `
            <div class="deck-key-icon">+</div>
            <div class="deck-key-label">Add Key</div>
        `;
        addBtn.onclick = () => openEditButtonModal(null);
        grid.appendChild(addBtn);
    }
}

function handleDeckKeyClick(idx, el) {
    if (state.isEditingGrid) {
        openEditButtonModal(idx);
        return;
    }

    const profile = state.profilesData.profiles[state.activeProfileId];
    const btn = profile.buttons[idx];
    if (!btn) return;

    if (btn.requires_confirmation) {
        showConfirmModal(
            `Confirm: ${btn.label}`,
            `This action will affect your Windows laptop (${btn.label}). Do you wish to proceed?`,
            () => executeAction(btn.action, { ...btn.params, confirmed: true }, el)
        );
    } else {
        executeAction(btn.action, btn.params || {}, el);
    }
}

function moveButton(idx, delta) {
    const profile = state.profilesData.profiles[state.activeProfileId];
    const newIdx = idx + delta;
    if (newIdx < 0 || newIdx >= profile.buttons.length) return;

    const temp = profile.buttons[idx];
    profile.buttons[idx] = profile.buttons[newIdx];
    profile.buttons[newIdx] = temp;

    saveProfilesToServer();
    renderActiveDeckGrid();
}

async function saveProfilesToServer() {
    await apiRequest('/api/v1/profiles', 'POST', state.profilesData);
}

// ==================== BUTTON MODAL ====================
function openEditButtonModal(idx) {
    state.editingButtonIndex = idx;
    const modal = document.getElementById('buttonModal');
    const title = document.getElementById('buttonModalTitle');
    const deleteBtn = document.getElementById('deleteButtonBtn');
    const profile = state.profilesData.profiles[state.activeProfileId];

    if (idx !== null && profile.buttons[idx]) {
        const btn = profile.buttons[idx];
        title.textContent = 'Edit Touch Key';
        document.getElementById('btnLabel').value = btn.label;
        document.getElementById('btnActionSelect').value = btn.action;
        document.getElementById('btnIcon').value = btn.icon || 'volume-2';
        document.getElementById('btnSize').value = btn.size || '1x1';
        deleteBtn.style.display = 'inline-flex';
        renderActionParamFields(btn.action, btn.params);
    } else {
        title.textContent = 'Add New Touch Key';
        document.getElementById('btnLabel').value = '';
        document.getElementById('btnActionSelect').value = 'set_volume';
        document.getElementById('btnIcon').value = 'volume-2';
        document.getElementById('btnSize').value = '1x1';
        deleteBtn.style.display = 'none';
        renderActionParamFields('set_volume', {});
    }

    modal.style.display = 'flex';
}

function renderActionParamFields(action, currentParams = {}) {
    const container = document.getElementById('btnParamContainer');
    currentParams = currentParams || {};

    if (action === 'set_volume') {
        container.innerHTML = `
            <label for="paramVolumeLevel">Volume Target Percentage (0 - 100)</label>
            <input type="number" id="paramVolumeLevel" min="0" max="100" value="${currentParams.level || 50}">
        `;
    } else if (action === 'volume_step') {
        container.innerHTML = `
            <label for="paramVolumeDelta">Volume Step Delta (+/- percent)</label>
            <input type="number" id="paramVolumeDelta" value="${currentParams.delta || 5}">
        `;
    } else if (action === 'media_transport') {
        container.innerHTML = `
            <label for="paramMediaAction">Media Transport Action</label>
            <select id="paramMediaAction">
                <option value="play_pause" ${currentParams.action === 'play_pause' ? 'selected' : ''}>Play / Pause</option>
                <option value="next" ${currentParams.action === 'next' ? 'selected' : ''}>Next Track</option>
                <option value="previous" ${currentParams.action === 'previous' ? 'selected' : ''}>Previous Track</option>
            </select>
        `;
    } else if (action === 'launch_app') {
        container.innerHTML = `
            <label for="paramAppId">Registered Application</label>
            <select id="paramAppId">
                <option value="antigravity" ${currentParams.app_id === 'antigravity' ? 'selected' : ''}>Antigravity IDE</option>
                <option value="chrome" ${currentParams.app_id === 'chrome' ? 'selected' : ''}>Google Chrome</option>
                <option value="terminal" ${currentParams.app_id === 'terminal' ? 'selected' : ''}>Windows Terminal</option>
                <option value="powershell" ${currentParams.app_id === 'powershell' ? 'selected' : ''}>PowerShell</option>
                <option value="whatsapp" ${currentParams.app_id === 'whatsapp' ? 'selected' : ''}>WhatsApp Desktop</option>
                <option value="explorer" ${currentParams.app_id === 'explorer' ? 'selected' : ''}>File Explorer</option>
                <option value="taskmgr" ${currentParams.app_id === 'taskmgr' ? 'selected' : ''}>Task Manager</option>
                <option value="settings" ${currentParams.app_id === 'settings' ? 'selected' : ''}>Windows Settings</option>
            </select>
        `;
    } else if (action === 'send_shortcut') {
        container.innerHTML = `
            <label for="paramShortcut">Approved Windows Shortcut</label>
            <select id="paramShortcut">
                <option value="Win+E" ${currentParams.shortcut === 'Win+E' ? 'selected' : ''}>Win + E (Explorer)</option>
                <option value="Win+Shift+S" ${currentParams.shortcut === 'Win+Shift+S' ? 'selected' : ''}>Win + Shift + S (Snip)</option>
                <option value="Ctrl+Shift+Esc" ${currentParams.shortcut === 'Ctrl+Shift+Esc' ? 'selected' : ''}>Ctrl + Shift + Esc (TaskMgr)</option>
                <option value="Alt+Tab" ${currentParams.shortcut === 'Alt+Tab' ? 'selected' : ''}>Alt + Tab (Switch Window)</option>
                <option value="Win+D" ${currentParams.shortcut === 'Win+D' ? 'selected' : ''}>Win + D (Desktop)</option>
                <option value="Ctrl+C" ${currentParams.shortcut === 'Ctrl+C' ? 'selected' : ''}>Ctrl + C (Copy)</option>
                <option value="Ctrl+V" ${currentParams.shortcut === 'Ctrl+V' ? 'selected' : ''}>Ctrl + V (Paste)</option>
                <option value="Ctrl+Z" ${currentParams.shortcut === 'Ctrl+Z' ? 'selected' : ''}>Ctrl + Z (Undo)</option>
                <option value="Ctrl+Shift+T" ${currentParams.shortcut === 'Ctrl+Shift+T' ? 'selected' : ''}>Ctrl + Shift + T (Reopen Tab)</option>
            </select>
        `;
    } else if (action === 'run_macro') {
        const macroOpts = Object.keys(state.macrosData).map(mId => {
            const m = state.macrosData[mId];
            return `<option value="${mId}" ${currentParams.macro_id === mId ? 'selected' : ''}>${escapeHtml(m.name)}</option>`;
        }).join('');
        container.innerHTML = `
            <label for="paramMacroId">Select Macro</label>
            <select id="paramMacroId">${macroOpts}</select>
        `;
    } else {
        container.innerHTML = '';
    }
}

// ==================== APPS PAGE ====================
async function loadApps() {
    const res = await apiRequest('/api/v1/apps');
    if (!res.ok || !res.apps) return;
    state.appsData = res.apps;

    const grid = document.getElementById('appsGrid');
    grid.innerHTML = res.apps.map(app => {
        let statusBadge = '';
        if (app.is_running) {
            statusBadge = '<span class="app-status-badge badge-running">● Running</span>';
        } else if (app.installed) {
            statusBadge = '<span class="app-status-badge badge-installed">Ready</span>';
        } else {
            statusBadge = '<span class="app-status-badge badge-missing">Missing</span>';
        }

        const iconSvg = ICONS[app.icon] || ICONS['monitor'];

        return `
            <div class="app-card" onclick="launchApp('${app.id}', this)">
                <div class="app-card-icon">${iconSvg}</div>
                <div class="app-card-info">
                    <div class="app-card-title">${escapeHtml(app.name)}</div>
                    <div class="app-card-desc">${escapeHtml(app.description || '')}</div>
                    ${statusBadge}
                </div>
            </div>
        `;
    }).join('');
}

async function launchApp(appId, cardEl) {
    if (cardEl) {
        cardEl.style.transform = 'scale(0.95)';
        setTimeout(() => cardEl.style.transform = '', 150);
    }
    const res = await apiRequest('/api/v1/apps/launch', 'POST', { app_id: appId });
    if (res.ok) {
        showToast(res.message || 'Launched application', 'success');
        refreshHistory();
        setTimeout(loadApps, 1000);
    } else {
        showToast(res.error || 'Failed to launch', 'error');
    }
}

// ==================== MACROS PAGE ====================
async function loadMacros() {
    const res = await apiRequest('/api/v1/macros');
    if (!res.ok || !res.macros) return;
    state.macrosData = res.macros;

    const list = document.getElementById('macrosList');
    const macros = res.macros;

    list.innerHTML = Object.keys(macros).map(mId => {
        const m = macros[mId];
        const stepCount = (m.actions || []).length;
        const iconSvg = ICONS[m.icon] || ICONS['sparkles'];

        return `
            <div class="macro-card">
                <div class="macro-card-left">
                    <div class="macro-icon-wrap">${iconSvg}</div>
                    <div>
                        <h4>${escapeHtml(m.name)}</h4>
                        <p class="section-subtitle">${escapeHtml(m.description || '')} (${stepCount} steps)</p>
                    </div>
                </div>
                <div class="macro-actions-cluster">
                    <button class="btn-primary btn-sm" onclick="runMacro('${mId}', this)">Run Macro</button>
                    <button class="btn-secondary btn-sm" onclick="openMacroEditor('${mId}')">Edit</button>
                    <button class="btn-danger btn-sm" onclick="deleteMacro('${mId}')">Delete</button>
                </div>
            </div>
        `;
    }).join('');
}

async function runMacro(macroId, btnEl) {
    if (btnEl) {
        btnEl.disabled = true;
        btnEl.textContent = 'Running...';
    }
    const res = await apiRequest('/api/v1/macros/run', 'POST', { macro_id: macroId });
    if (btnEl) {
        btnEl.disabled = false;
        btnEl.textContent = 'Run Macro';
    }
    if (res.ok) {
        showToast(res.message || 'Macro completed', 'success');
        refreshHistory();
        pollStatus();
    } else {
        showToast(res.error || 'Macro failed', 'error');
    }
}

async function deleteMacro(macroId) {
    showConfirmModal(
        'Delete Macro',
        `Are you sure you want to delete macro '${macroId}'?`,
        async () => {
            const res = await apiRequest(`/api/v1/macros/${macroId}`, 'DELETE');
            if (res.ok) {
                showToast('Macro deleted', 'info');
                loadMacros();
            }
        }
    );
}

let activeMacroEditing = null;

function openMacroEditor(macroId = null) {
    activeMacroEditing = macroId ? JSON.parse(JSON.stringify(state.macrosData[macroId])) : {
        id: `macro_${Date.now()}`,
        name: '',
        description: '',
        icon: 'sparkles',
        actions: []
    };

    document.getElementById('macroName').value = activeMacroEditing.name || '';
    document.getElementById('macroDesc').value = activeMacroEditing.description || '';
    renderMacroStepsList();
    document.getElementById('macroModal').style.display = 'flex';
}

function renderMacroStepsList() {
    const container = document.getElementById('macroStepsContainer');
    if (!activeMacroEditing || !activeMacroEditing.actions) return;

    container.innerHTML = activeMacroEditing.actions.map((act, idx) => {
        return `
            <div class="macro-step-row">
                <span class="step-num">#${idx + 1}</span>
                <select onchange="updateMacroStepType(${idx}, this.value)" style="flex: 1;">
                    <option value="launch_app" ${act.type === 'launch_app' ? 'selected' : ''}>Launch Application</option>
                    <option value="set_volume" ${act.type === 'set_volume' ? 'selected' : ''}>Set Volume Level</option>
                    <option value="media_transport" ${act.type === 'media_transport' ? 'selected' : ''}>Media Control</option>
                    <option value="send_shortcut" ${act.type === 'send_shortcut' ? 'selected' : ''}>Keyboard Shortcut</option>
                    <option value="delay" ${act.type === 'delay' ? 'selected' : ''}>Wait / Delay</option>
                    <option value="show_desktop" ${act.type === 'show_desktop' ? 'selected' : ''}>Show Desktop</option>
                </select>
                <div id="macroStepParam_${idx}" style="flex: 1;">
                    ${getMacroStepParamInput(act, idx)}
                </div>
                <button type="button" class="btn-icon-compact" onclick="removeMacroStep(${idx})" title="Remove">&times;</button>
            </div>
        `;
    }).join('');
}

function getMacroStepParamInput(act, idx) {
    if (act.type === 'launch_app') {
        return `
            <select onchange="activeMacroEditing.actions[${idx}].target = this.value">
                <option value="antigravity" ${act.target === 'antigravity' ? 'selected' : ''}>Antigravity IDE</option>
                <option value="chrome" ${act.target === 'chrome' ? 'selected' : ''}>Google Chrome</option>
                <option value="terminal" ${act.target === 'terminal' ? 'selected' : ''}>Windows Terminal</option>
                <option value="powershell" ${act.target === 'powershell' ? 'selected' : ''}>PowerShell</option>
            </select>
        `;
    } else if (act.type === 'set_volume') {
        return `<input type="number" min="0" max="100" value="${act.level || 30}" onchange="activeMacroEditing.actions[${idx}].level = parseInt(this.value)">`;
    } else if (act.type === 'delay') {
        return `<input type="number" step="0.1" min="0.1" max="5.0" value="${act.seconds || 0.5}" onchange="activeMacroEditing.actions[${idx}].seconds = parseFloat(this.value)">`;
    } else if (act.type === 'media_transport') {
        return `
            <select onchange="activeMacroEditing.actions[${idx}].action = this.value">
                <option value="play_pause" ${act.action === 'play_pause' ? 'selected' : ''}>Play / Pause</option>
                <option value="next" ${act.action === 'next' ? 'selected' : ''}>Next</option>
                <option value="previous" ${act.action === 'previous' ? 'selected' : ''}>Previous</option>
            </select>
        `;
    } else if (act.type === 'send_shortcut') {
        return `
            <select onchange="activeMacroEditing.actions[${idx}].shortcut = this.value">
                <option value="Win+E" ${act.shortcut === 'Win+E' ? 'selected' : ''}>Win + E</option>
                <option value="Win+Shift+S" ${act.shortcut === 'Win+Shift+S' ? 'selected' : ''}>Win + Shift + S</option>
                <option value="Alt+Tab" ${act.shortcut === 'Alt+Tab' ? 'selected' : ''}>Alt + Tab</option>
                <option value="Ctrl+Shift+Esc" ${act.shortcut === 'Ctrl+Shift+Esc' ? 'selected' : ''}>Ctrl + Shift + Esc</option>
            </select>
        `;
    }
    return '';
}

function updateMacroStepType(idx, newType) {
    if (!activeMacroEditing || !activeMacroEditing.actions[idx]) return;
    const step = { type: newType };
    if (newType === 'launch_app') step.target = 'antigravity';
    if (newType === 'set_volume') step.level = 30;
    if (newType === 'delay') step.seconds = 0.5;
    if (newType === 'media_transport') step.action = 'play_pause';
    if (newType === 'send_shortcut') step.shortcut = 'Win+E';
    activeMacroEditing.actions[idx] = step;
    renderMacroStepsList();
}

function removeMacroStep(idx) {
    activeMacroEditing.actions.splice(idx, 1);
    renderMacroStepsList();
}

// ==================== PROFILES MANAGER ====================
function renderProfilesManager() {
    if (!state.profilesData) return;
    const grid = document.getElementById('profilesCardsList');
    const profiles = state.profilesData.profiles;

    grid.innerHTML = Object.keys(profiles).map(id => {
        const p = profiles[id];
        const isCurrent = id === state.activeProfileId;
        const btnCount = (p.buttons || []).length;

        return `
            <div class="profile-manage-card">
                <div class="profile-card-header">
                    <h4>${escapeHtml(p.name)}</h4>
                    ${isCurrent ? '<span class="badge-status status-ready">Active</span>' : ''}
                </div>
                <p class="section-subtitle">${escapeHtml(p.description || '')}</p>
                <p class="section-subtitle">Total Keys: <strong>${btnCount}</strong></p>
                <div class="profile-card-btns">
                    ${!isCurrent ? `<button class="btn-primary btn-sm" onclick="switchProfile('${id}')">Activate</button>` : ''}
                    <button class="btn-secondary btn-sm" onclick="duplicateProfile('${id}')">Duplicate</button>
                    ${!p.is_builtin ? `<button class="btn-danger btn-sm" onclick="deleteProfile('${id}')">Delete</button>` : ''}
                </div>
            </div>
        `;
    }).join('');
}

function switchProfile(profileId) {
    state.activeProfileId = profileId;
    localStorage.setItem('dex_active_profile', profileId);
    renderHeaderProfileSelect();
    renderActiveDeckGrid();
    renderProfilesManager();
    showToast(`Switched to ${profileId} profile`, 'info');
}

function duplicateProfile(profileId) {
    const src = state.profilesData.profiles[profileId];
    if (!src) return;
    const newId = `profile_${Date.now()}`;
    state.profilesData.profiles[newId] = {
        ...JSON.parse(JSON.stringify(src)),
        id: newId,
        name: `${src.name} (Copy)`,
        is_builtin: false
    };
    saveProfilesToServer();
    renderHeaderProfileSelect();
    renderProfilesManager();
    showToast('Profile duplicated', 'success');
}

function deleteProfile(profileId) {
    showConfirmModal(
        'Delete Profile',
        `Are you sure you want to delete profile '${profileId}'?`,
        () => {
            delete state.profilesData.profiles[profileId];
            if (state.activeProfileId === profileId) {
                state.activeProfileId = 'general';
            }
            saveProfilesToServer();
            renderHeaderProfileSelect();
            renderActiveDeckGrid();
            renderProfilesManager();
            showToast('Profile deleted', 'info');
        }
    );
}

// ==================== SCREENSHOT PREVIEW ====================
async function triggerScreenshot() {
    showToast('Capturing Windows screen...', 'info');
    const res = await executeAction('screenshot', {});
    if (res.ok && res.result && res.result.url) {
        const modal = document.getElementById('screenshotModal');
        const img = document.getElementById('screenshotPreviewImg');
        const dl = document.getElementById('screenshotDownloadLink');
        img.src = `${res.result.url}?t=${Date.now()}`;
        dl.href = res.result.url;
        modal.style.display = 'flex';
    }
}

// ==================== CONFIRM MODAL ====================
function showConfirmModal(title, msg, onConfirm) {
    const modal = document.getElementById('confirmModal');
    document.getElementById('confirmModalTitle').textContent = title;
    document.getElementById('confirmModalMessage').textContent = msg;

    const proceedBtn = document.getElementById('confirmModalProceed');
    const cancelBtn = document.getElementById('confirmModalCancel');

    const cleanUp = () => {
        modal.style.display = 'none';
        proceedBtn.onclick = null;
        cancelBtn.onclick = null;
    };

    proceedBtn.onclick = () => {
        cleanUp();
        onConfirm();
    };
    cancelBtn.onclick = cleanUp;
    modal.style.display = 'flex';
}

function escapeHtml(str) {
    if (!str) return '';
    return String(str).replace(/[&<>"']/g, m => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    }[m]));
}

// ==================== INITIALIZATION & EVENT LISTENERS ====================
document.addEventListener('DOMContentLoaded', () => {
    // Navigation Tabs
    document.querySelectorAll('.nav-tab').forEach(tab => {
        tab.addEventListener('click', () => {
            const pageId = tab.dataset.page;
            document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.view-page').forEach(p => p.classList.remove('active'));
            tab.classList.add('active');
            const targetPage = document.getElementById(`page-${pageId}`);
            if (targetPage) targetPage.classList.add('active');

            if (pageId === 'apps') loadApps();
            if (pageId === 'macros') loadMacros();
            if (pageId === 'profiles') renderProfilesManager();
        });
    });

    // Profile select in header
    document.getElementById('headerProfileSelect').addEventListener('change', (e) => {
        switchProfile(e.target.value);
    });

    // Edit Layout Toggle
    document.getElementById('editLayoutBtn').addEventListener('click', () => {
        state.isEditingGrid = !state.isEditingGrid;
        const btn = document.getElementById('editLayoutBtn');
        btn.querySelector('span').textContent = state.isEditingGrid ? 'Done Editing' : 'Edit Grid';
        btn.className = state.isEditingGrid ? 'btn-primary btn-sm' : 'btn-secondary btn-sm';
        renderActiveDeckGrid();
    });

    // Theme Toggle
    document.getElementById('themeToggleBtn').addEventListener('click', () => {
        const html = document.documentElement;
        const current = html.getAttribute('data-theme') || 'dark';
        const next = current === 'dark' ? 'light' : 'dark';
        html.setAttribute('data-theme', next);
        localStorage.setItem('dex_theme', next);
    });

    const savedTheme = localStorage.getItem('dex_theme') || localStorage.getItem('fury_theme');
    if (savedTheme) {
        document.documentElement.setAttribute('data-theme', savedTheme);
    }

    // Quick Screenshot in header
    document.getElementById('quickShotBtn').addEventListener('click', triggerScreenshot);
    document.getElementById('closeScreenshotModal').addEventListener('click', () => {
        document.getElementById('screenshotModal').style.display = 'none';
    });
    document.getElementById('closeScreenshotBtn').addEventListener('click', () => {
        document.getElementById('screenshotModal').style.display = 'none';
    });

    // Volume Sliders (real-time responsive sync)
    const homeSlider = document.getElementById('homeVolumeSlider');
    const mediaSlider = document.getElementById('mediaVolumeSlider');
    let volumeTimeout = null;

    function handleSliderChange(val) {
        state.isDraggingVolume = true;
        const volNum = Math.max(0, Math.min(100, parseInt(val) || 0));
        updateVolumeUI(volNum, false);
        clearTimeout(volumeTimeout);
        volumeTimeout = setTimeout(async () => {
            const res = await apiRequest('/api/v1/volume', 'POST', { level: volNum });
            if (res && res.ok && typeof res.volume === 'number') {
                updateVolumeUI(res.volume, res.is_muted);
            }
        }, 50);
    }

    const onSliderRelease = () => {
        setTimeout(() => {
            state.isDraggingVolume = false;
        }, 200);
    };

    homeSlider.addEventListener('input', (e) => handleSliderChange(e.target.value));
    mediaSlider.addEventListener('input', (e) => handleSliderChange(e.target.value));
    homeSlider.addEventListener('change', onSliderRelease);
    mediaSlider.addEventListener('change', onSliderRelease);
    homeSlider.addEventListener('pointerup', onSliderRelease);
    mediaSlider.addEventListener('pointerup', onSliderRelease);
    homeSlider.addEventListener('touchend', onSliderRelease);
    mediaSlider.addEventListener('touchend', onSliderRelease);

    // Volume Presets
    document.querySelectorAll('.btn-preset, .btn-preset-card').forEach(btn => {
        btn.addEventListener('click', () => {
            const vol = parseInt(btn.dataset.vol);
            executeAction('set_volume', { level: vol });
        });
    });

    // Mute Toggles
    const toggleMute = () => executeAction('set_mute', {});
    document.getElementById('quickMuteBtn').addEventListener('click', toggleMute);
    document.getElementById('homeMuteToggle').addEventListener('click', toggleMute);
    document.getElementById('mediaMuteBtn').addEventListener('click', toggleMute);

    // Media Transport Buttons
    document.getElementById('mediaPlayPauseBtn').addEventListener('click', () => executeAction('media_transport', { action: 'play_pause' }));
    document.getElementById('mediaNextBtn').addEventListener('click', () => executeAction('media_transport', { action: 'next' }));
    document.getElementById('mediaPrevBtn').addEventListener('click', () => executeAction('media_transport', { action: 'previous' }));
    document.getElementById('mediaRewindBtn').addEventListener('click', () => executeAction('media_transport', { action: 'rewind' }));
    document.getElementById('mediaFastForwardBtn').addEventListener('click', () => executeAction('media_transport', { action: 'fast_forward' }));

    // Button Modal Events
    document.getElementById('btnActionSelect').addEventListener('change', (e) => {
        renderActionParamFields(e.target.value, {});
    });
    document.getElementById('closeButtonModal').addEventListener('click', () => {
        document.getElementById('buttonModal').style.display = 'none';
    });
    document.getElementById('cancelButtonModal').addEventListener('click', () => {
        document.getElementById('buttonModal').style.display = 'none';
    });
    document.getElementById('deleteButtonBtn').addEventListener('click', () => {
        if (state.editingButtonIndex !== null) {
            const profile = state.profilesData.profiles[state.activeProfileId];
            profile.buttons.splice(state.editingButtonIndex, 1);
            saveProfilesToServer();
            renderActiveDeckGrid();
            document.getElementById('buttonModal').style.display = 'none';
        }
    });

    document.getElementById('buttonForm').addEventListener('submit', (e) => {
        e.preventDefault();
        const profile = state.profilesData.profiles[state.activeProfileId];
        const action = document.getElementById('btnActionSelect').value;
        const label = document.getElementById('btnLabel').value;
        const icon = document.getElementById('btnIcon').value;
        const size = document.getElementById('btnSize').value;

        // Collect params based on action
        const params = {};
        if (action === 'set_volume') {
            params.level = parseInt(document.getElementById('paramVolumeLevel').value);
        } else if (action === 'volume_step') {
            params.delta = parseInt(document.getElementById('paramVolumeDelta').value);
        } else if (action === 'media_transport') {
            params.action = document.getElementById('paramMediaAction').value;
        } else if (action === 'launch_app') {
            params.app_id = document.getElementById('paramAppId').value;
        } else if (action === 'send_shortcut') {
            params.shortcut = document.getElementById('paramShortcut').value;
        } else if (action === 'run_macro') {
            params.macro_id = document.getElementById('paramMacroId').value;
        }

        const btnObj = {
            id: `btn_${Date.now()}`,
            label,
            icon,
            category: 'custom',
            action,
            params,
            size,
            requires_confirmation: action === 'lock_pc'
        };

        if (state.editingButtonIndex !== null) {
            profile.buttons[state.editingButtonIndex] = btnObj;
        } else {
            profile.buttons.push(btnObj);
        }

        saveProfilesToServer();
        renderActiveDeckGrid();
        document.getElementById('buttonModal').style.display = 'none';
        showToast('Touch key saved', 'success');
    });

    // Macro Step Actions
    document.getElementById('addMacroStepBtn').addEventListener('click', () => {
        if (!activeMacroEditing.actions) activeMacroEditing.actions = [];
        if (activeMacroEditing.actions.length >= 10) {
            showToast('Maximum 10 actions allowed per macro', 'error');
            return;
        }
        activeMacroEditing.actions.push({ type: 'delay', seconds: 0.5 });
        renderMacroStepsList();
    });

    document.getElementById('testRunMacroBtn').addEventListener('click', async () => {
        if (!activeMacroEditing || !activeMacroEditing.actions.length) return;
        // Temporarily save and run
        activeMacroEditing.name = document.getElementById('macroName').value || 'Test Run';
        activeMacroEditing.description = document.getElementById('macroDesc').value;
        const saveRes = await apiRequest('/api/v1/macros', 'POST', activeMacroEditing);
        if (saveRes.ok) {
            runMacro(activeMacroEditing.id);
        }
    });

    document.getElementById('macroForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        activeMacroEditing.name = document.getElementById('macroName').value;
        activeMacroEditing.description = document.getElementById('macroDesc').value;

        const res = await apiRequest('/api/v1/macros', 'POST', activeMacroEditing);
        if (res.ok) {
            document.getElementById('macroModal').style.display = 'none';
            showToast('Macro saved', 'success');
            loadMacros();
        } else {
            showToast(res.message || 'Macro save failed', 'error');
        }
    });
    document.getElementById('closeMacroModal').addEventListener('click', () => {
        document.getElementById('macroModal').style.display = 'none';
    });
    document.getElementById('cancelMacroModal').addEventListener('click', () => {
        document.getElementById('macroModal').style.display = 'none';
    });
    document.getElementById('createMacroBtn').addEventListener('click', () => openMacroEditor(null));

    // Custom App Modal
    document.getElementById('addCustomAppBtn').addEventListener('click', () => {
        document.getElementById('customAppModal').style.display = 'flex';
    });
    document.getElementById('closeCustomAppModal').addEventListener('click', () => {
        document.getElementById('customAppModal').style.display = 'none';
    });
    document.getElementById('cancelCustomAppModal').addEventListener('click', () => {
        document.getElementById('customAppModal').style.display = 'none';
    });
    document.getElementById('customAppForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const id = document.getElementById('customAppId').value;
        const name = document.getElementById('customAppName').value;
        const path = document.getElementById('customAppPath').value;
        const category = document.getElementById('customAppCategory').value;

        const res = await apiRequest('/api/v1/settings/custom-app', 'POST', { id, name, path, category });
        if (res.ok) {
            document.getElementById('customAppModal').style.display = 'none';
            showToast('Executable registered', 'success');
            loadApps();
        } else {
            showToast(res.message || 'Registration failed', 'error');
        }
    });

    // Settings Network & LAN
    async function loadSettingsUI() {
        const res = await apiRequest('/api/v1/settings');
        if (res.ok && res.settings) {
            document.getElementById('lanToggle').checked = bool(res.settings.lan_enabled);
            document.getElementById('settingsLanIp').textContent = res.lan_ip || '127.0.0.1';
            document.getElementById('settingsFullUrl').textContent = `http://${res.lan_ip || '127.0.0.1'}:5000`;
            document.getElementById('guideUrl').textContent = `http://${res.lan_ip || '127.0.0.1'}:5000`;
            document.getElementById('settingsPairingPin').textContent = res.pairing_pin || '------';

            const paths = res.settings.app_paths || {};
            if (paths.antigravity) document.getElementById('pathAntigravity').value = paths.antigravity;
            if (paths.chrome) document.getElementById('pathChrome').value = paths.chrome;
            if (paths.terminal) document.getElementById('pathTerminal').value = paths.terminal;
        }
    }

    function bool(v) { return v === true || v === 'true'; }

    document.getElementById('lanToggle').addEventListener('change', async (e) => {
        const enabled = e.target.checked;
        const res = await apiRequest('/api/v1/settings', 'POST', { lan_enabled: enabled });
        if (res.ok) {
            showToast(`LAN Access ${enabled ? 'Enabled' : 'Disabled'}. Restart server to apply interface bind change.`, 'info');
        }
    });

    document.getElementById('regenPinBtn').addEventListener('click', async () => {
        const res = await apiRequest('/api/v1/settings/regenerate-pin', 'POST');
        if (res.ok && res.pairing_pin) {
            document.getElementById('settingsPairingPin').textContent = res.pairing_pin;
            showToast('New iPad pairing PIN generated', 'success');
        }
    });

    document.getElementById('changePasswordForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const current_password = document.getElementById('currentPwd').value;
        const new_password = document.getElementById('newPwd').value;
        const res = await apiRequest('/api/v1/settings/password', 'POST', { current_password, new_password });
        if (res.ok) {
            showToast('Password updated', 'success');
            document.getElementById('changePasswordForm').reset();
        } else {
            showToast(res.message || 'Update failed', 'error');
        }
    });

    document.getElementById('appPathsForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const app_paths = {
            antigravity: document.getElementById('pathAntigravity').value,
            chrome: document.getElementById('pathChrome').value,
            terminal: document.getElementById('pathTerminal').value
        };
        const res = await apiRequest('/api/v1/settings', 'POST', { app_paths });
        if (res.ok) {
            showToast('Application paths updated', 'success');
        }
    });

    document.getElementById('logoutBtn').addEventListener('click', async () => {
        await apiRequest('/api/v1/auth/logout', 'POST');
        window.location.href = '/login';
    });

    document.getElementById('resetDefaultsBtn').addEventListener('click', () => {
        showConfirmModal(
            'Restore Defaults',
            'Restore all profiles to factory defaults? Custom layouts will be reset.',
            async () => {
                const res = await apiRequest('/api/v1/profiles/reset', 'POST');
                if (res.ok) {
                    state.profilesData = res.profiles;
                    renderHeaderProfileSelect();
                    renderActiveDeckGrid();
                    renderProfilesManager();
                    showToast('Defaults restored', 'success');
                }
            }
        );
    });

    // Start initial loading and polling loop
    loadProfiles();
    pollStatus();
    loadSettingsUI();
    refreshHistory();
    state.pollTimer = setInterval(pollStatus, 2500);
});
