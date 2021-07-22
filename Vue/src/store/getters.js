import { widgetTemplate } from './workspace';

export let workspace = (state) => (id) => state.workspaces.find((workspace) => workspace.id === id);

export let widget = (state) => (workspace_id, widget_id) =>
	workspace(state)(workspace_id).widgets.find((widget) => widget.id === widget_id);

export let widget_template = (state) => (id, type) => widgetTemplate(workspace(state)(id).widget_index, type);
