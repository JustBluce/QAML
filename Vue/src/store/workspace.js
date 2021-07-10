export function widgetTemplate(id, type) {
	let widget_templates = {
		Timer: {
			id: id,
			title: 'Timer',
			type: 'Timer',
			container: 'left',
			expanded: true,
			maxHeight: '200px'
		},
		Pronunciation: {
			id: id,
			title: 'Pronunciation difficulty',
			type: 'Pronunciation',
			container: 'left',
			expanded: true,
			maxHeight: '250px'
		},
		Representation: {
			id: id,
			title: 'Representation analysis',
			type: 'Representation',
			container: 'right',
			expanded: true,
			maxHeight: '300px'
		}
	};
	return widget_templates[type];
}

export function defaultWorkspace(id) {
	return {
		id: id,
		title: 'Workspace',
		qas: [
			{
				id: 0,
				title: 'QA',
				text: '',
				country_representation: '',
				people_ethnicity: ''
			}
		],
		qa_index: 1,
		qa_selected: 0,
		widgets: [
			widgetTemplate(0, 'Timer'),
			widgetTemplate(1, 'Pronunciation'),
			widgetTemplate(2, 'Representation')
		],
		widget_index: 3,
		style: {
			left: 0,
			top: 0
		}
	};
}

export function defaultQA(id) {
	return {
		id: id,
		title: `QA (${id})`,
		text: '',
		country_representation: '',
		people_ethnicity: ''
	};
}

export const initial_workspaces = [ defaultWorkspace(0) ];
