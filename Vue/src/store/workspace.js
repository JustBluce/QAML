export function defaultWorkspace(id) {
	return {
		id: id,
		qas: [
			{
				id: 0,
				title: "QA",
				text: "",
			}
		],
		qa_selected: 0,
		widgets: [
		],
		widget_index: 0,
	};
}

export const initial_workspaces = [ defaultWorkspace(0) ];
