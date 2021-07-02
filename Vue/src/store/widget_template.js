export function widgetTemplate(workspace, type) {
	let widget_templates = {
		QA: {
			id: workspace.widget_index,
			title: 'QA',
			type: 'QA',
			expanded: true,
			autosave: true,
			maxHeight: '350px',
			maxWidth: '800px',
			text: ''
		},
		Timer: {
			id: workspace.widget_index,
			title: 'Timer',
			type: 'Timer',
			expanded: true,
			readonly: true,
			maxHeight: '200px',
			maxWidth: '464px'
		},
		Pronunciation: {
			id: workspace.widget_index,
			title: 'Pronunciation difficulty',
			type: 'Pronunciation',
			expanded: true,
			readonly: true,
			maxHeight: '250px',
			maxWidth: '800px',
			qa_id: 0
		}
	};
	return widget_templates[type];
}
