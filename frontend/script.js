const API_BASE_URL = window.location.origin;

// Determine if we're running locally with uvicorn vs deployed
const getApiUrl = () => {
    // If running on file:// or port 5500 (Live Server), assume backend is on 8000
    if (window.location.protocol === 'file:' || window.location.port === '5500') {
        return 'http://localhost:8000';
    }
    return API_BASE_URL;
};

const API = getApiUrl();

async function fetchStats() {
    try {
        const res = await fetch(`${API}/dashboard/stats`);
        const data = await res.json();
        document.getElementById('stat-active').innerText = data.active_count;
        document.getElementById('stat-expired').innerText = data.expired_count;
    } catch (err) {
        console.error("Error fetching stats:", err);
    }
}

async function fetchAlerts() {
    try {
        const res = await fetch(`${API}/alerts/expiring-soon`);
        const alerts = await res.json();
        
        document.getElementById('stat-expiring-soon').innerText = alerts.length;
        
        const container = document.getElementById('alerts-container');
        container.innerHTML = '';
        
        if (alerts.length === 0) {
            container.innerHTML = '<div class="text-gray-500 text-sm italic">No certifications expiring soon.</div>';
            return;
        }

        alerts.forEach(alert => {
            container.innerHTML += `
                <div class="p-4 bg-obsidian-900 border border-amber-900/30 rounded-lg flex justify-between items-center group hover:border-amber-700/50 transition-colors">
                    <div>
                        <p class="text-white font-medium text-sm">${alert.user_name}</p>
                        <p class="text-amber-400 text-xs">${alert.certification_name}</p>
                    </div>
                    <div class="text-right flex flex-col items-end">
                        <p class="text-gray-400 text-xs mb-1">Expires: ${alert.expiry_date}</p>
                        ${alert.credential_url ? `<a href="${alert.credential_url}" target="_blank" class="text-xs text-accent-400 hover:text-accent-300">View Credential &rarr;</a>` : ''}
                    </div>
                </div>
            `;
        });
    } catch (err) {
        console.error("Error fetching alerts:", err);
    }
}

async function fetchUserCerts() {
    try {
        const res = await fetch(`${API}/user-certifications/`);
        const certs = await res.json();
        
        const tbody = document.getElementById('cert-table-body');
        tbody.innerHTML = '';
        
        if (certs.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="px-4 py-4 text-center italic text-gray-600">No certifications found.</td></tr>';
            return;
        }

        const today = new Date();

        certs.forEach(c => {
            const expiry = new Date(c.expiry_date);
            const isExpired = expiry < today;
            const statusBadge = isExpired 
                ? '<span class="px-2 py-1 bg-rose-500/10 text-rose-400 rounded text-xs">Expired</span>'
                : '<span class="px-2 py-1 bg-emerald-500/10 text-emerald-400 rounded text-xs">Active</span>';

            tbody.innerHTML += `
                <tr class="hover:bg-obsidian-900/50 transition-colors">
                    <td class="px-4 py-3 text-white">#${c.id}</td>
                    <td class="px-4 py-3">${c.user_id}</td>
                    <td class="px-4 py-3">${c.certification_id}</td>
                    <td class="px-4 py-3">${c.expiry_date}</td>
                    <td class="px-4 py-3">${statusBadge}</td>
                </tr>
            `;
        });
    } catch (err) {
        console.error("Error fetching user certs:", err);
    }
}

async function refreshDashboard() {
    await Promise.all([fetchStats(), fetchAlerts(), fetchUserCerts()]);
}

// Form Submission Handlers
document.getElementById('form-user').addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
        name: document.getElementById('user-name').value,
        email: document.getElementById('user-email').value
    };
    
    try {
        const res = await fetch(`${API}/users/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        if (res.ok) {
            alert('User added successfully!');
            e.target.reset();
        } else {
            alert('Failed to add user');
        }
    } catch (err) {
        console.error(err);
    }
});

document.getElementById('form-org').addEventListener('submit', async (e) => {
    e.preventDefault();
    try {
        const res = await fetch(`${API}/organizations/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: document.getElementById('org-name').value })
        });
        if (res.ok) { alert('Organization added!'); e.target.reset(); }
    } catch (err) { console.error(err); }
});

document.getElementById('form-cert').addEventListener('submit', async (e) => {
    e.preventDefault();
    try {
        const res = await fetch(`${API}/certifications/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                name: document.getElementById('cert-name').value,
                organization_id: parseInt(document.getElementById('cert-org-id').value)
            })
        });
        if (res.ok) { alert('Certification added!'); e.target.reset(); }
    } catch (err) { console.error(err); }
});

document.getElementById('form-user-cert').addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
        user_id: parseInt(document.getElementById('uc-user-id').value),
        certification_id: parseInt(document.getElementById('uc-cert-id').value),
        issue_date: document.getElementById('uc-issue').value,
        expiry_date: document.getElementById('uc-expiry').value,
        credential_url: document.getElementById('uc-url').value || null
    };
    
    try {
        const res = await fetch(`${API}/user-certifications/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        if (res.ok) {
            alert('Certification linked successfully!');
            e.target.reset();
            refreshDashboard();
        } else {
            alert('Failed to link certification');
        }
    } catch (err) {
        console.error(err);
    }
});

// Initial Load
document.addEventListener('DOMContentLoaded', refreshDashboard);
