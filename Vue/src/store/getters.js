export let workspace = (state) => (id) => state.workspaces.find((workspace) => workspace.id === id);
