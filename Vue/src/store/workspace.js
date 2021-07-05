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
			{
				id: 0,
				title: 'Timer',
				type: 'Timer',
				expanded: true,
				maxHeight: '200px',
			},
		],
		widget_index: 1,
	};
}

export const initial_workspaces = [ defaultWorkspace(0) ];
