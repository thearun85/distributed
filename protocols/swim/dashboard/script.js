NODES = [
	{"id": "node-1", "port": 6001},
	{"id": "node-2", "port": 6002},
	{"id": "node-3", "port": 6003},
]

function createNodeCard(nodeId) {
	containerDiv = document.getElementById("nodes");
	containerDiv.innerHTML += `
		<div class="node-card">
			<div class="node-header">${nodeId}</div>
			<div class="node-info" id="info-${nodeId}">Loading..</div>
			<div class="members" id="member-${nodeId}"></div>
		</div>
	`;
}

function markNodeOffline(nodeId) {
	infoDiv = document.getElementById(`info-${nodeId}`);
	memberDiv = document.getElementById(`member-${nodeId}`);
	infoDiv.innerHTML = "OFFLINE";
	memberDiv.innerHTML = "";
}

function updateNodeCard(nodeData) {
	nodeId = nodeData.node;
	infoDiv = document.getElementById(`info-${nodeId}`);
	memberDiv = document.getElementById(`member-${nodeId}`);
	infoDiv.innerHTML = `Port - ${nodeData.port}`;
	let membersHtml = `<strong>Known Members</strong>`;
	for (const [mId, member] of Object.entries(nodeData.members)) {
		membersHtml+= `
			<div class="member state-${member.state}">
				${mId}:${member.state}
			</div>
		`;
	}
	memberDiv.innerHTML = membersHtml;
}

async function fetchNodeState(port) {
	try {
		const response = await fetch(`http://localhost:${port}/state`)
		return await response.json();
	} catch (error) {
		return null;
	}
}
async function updateDashboard() {
	for (const node of NODES) {
		state = await fetchNodeState(node.port)
		if (state) {
			updateNodeCard(state);
			
		} else {
			markNodeOffline(node.id);
		}
	}
}

NODES.forEach( node => {
	createNodeCard(node.id);
})

updateDashboard();
