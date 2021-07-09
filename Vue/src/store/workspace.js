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
				container: 'left',
				expanded: true,
				maxHeight: '200px'
			},
			{
				id: 1,
				title: 'Pronunciation difficulty',
				type: 'Pronunciation',
				container: 'left',
				expanded: true,
				maxHeight: '250px',
			},
			{
				id: 2,
				title: 'Representation analysis',
				type: 'Representation',
				container: 'right',
				expanded: true,
				maxHeight: '300px',
			}
		],
		widget_index: 3
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
			container: 'left',
			expanded: true,
			maxHeight: '200px',
		},
		Pronunciation: {
			id: workspace.widget_index,
			title: 'Pronunciation difficulty',
			type: 'Pronunciation',
			container: 'left',
			expanded: true,
			maxHeight: '250px',
		},
		Representation: {
			id: workspace.widget_index,
			title: 'Representation analysis',
			type: 'Representation',
			container: 'right',
			expanded: true,
			maxHeight: '300px',
		}
	};
	return widget_templates[type];
}
