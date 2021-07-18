import { widgetTemplate } from './workspace.js';

export let workspace = (state) => (id) => state.workspaces.find((workspace) => workspace.id === id);

export let widget = (state) => (workspace_id, widget_id) =>
	workspace(state)(workspace_id).widgets.find((widget) => widget.id === widget_id);

export let widget_template = (state) => (id, type) => widgetTemplate(workspace(state)(id), type);

export let qa = (state) => (workspace_id, qa_id) => workspace(state)(workspace_id).qas.find((qa) => qa.id === qa_id);
