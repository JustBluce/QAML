export function defaultWorkspace(id) {
	return {
		id: id,
		qas: [
			{
				id: 0,
				title: 'QA',
				text: '',
				country_representation: '',
				people_ethnicity: '',
			}
		],
		qa_index: 1,
		qa_selected: 0,
		widgets: [
			{
				id: 0,
				title: 'Timer',
				type: 'Timer',
				expanded: true,
				maxHeight: '200px'
			}
		],
		widget_index: 1
	};
}

export function defaultQA(id) {
	return {
		id: id,
		title: `QA (${id})`,
		text: '',
		country_representation: '',
		people_ethnicity: '',
	}
}

export const initial_workspaces = [ defaultWorkspace(0) ];

export function widgetTemplate(workspace, type) {
	let widget_templates = {
		Timer: {
			id: workspace.widget_index,
			title: 'Timer',
			type: 'Timer',
			expanded: true,
			maxHeight: '200px',
		},
		Pronunciation: {
			id: workspace.widget_index,
			title: 'Pronunciation difficulty',
			type: 'Pronunciation',
			expanded: true,
			maxHeight: '250px',
		},
		Representation: {
			id: workspace.widget_index,
			title: 'Representation analysis',
			type: 'Representation',
			expanded: true,
			maxHeight: '300px',
		}
	};
	return widget_templates[type];
}
