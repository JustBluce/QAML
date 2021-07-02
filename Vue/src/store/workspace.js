export function defaultWorkspace(id) {
	return {
		id: id,
		widgets: [
			{
				id: 0,
				title: 'QA',
				type: 'QA',
				expanded: true,
				autosave: true,
				maxHeight: '350px',
				maxWidth: '800px',
				text: ''
			}
		],
		widget_index: 1
	};
}

export const initial_workspaces = [ defaultWorkspace(0) ];
