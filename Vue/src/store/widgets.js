export const initial_widgets = [
	{
		id: 0,
		title: 'QA1',
		type: 'QA',
		removable: false,
		expanded: true,
		maxHeight: '350px',
		maxWidth: '800px',
		text: ''
	},
	{
		id: 1,
		title: 'Timer',
		type: 'Timer',
		removable: true,
		expanded: true,
		maxHeight: '200px',
		maxWidth: '464px'
	},
	{
		id: 2,
		title: 'Pronunciation difficulty',
		type: 'Pronunciation',
		removable: true,
		expanded: true,
		maxHeight: '250px',
		maxWidth: '800px',
		qa_id: 0
	}
];

export const widget_types = [ 'QA', 'Timer', 'Pronunciation' ];

export function widgetTemplate(state, type) {
	let widget_templates = {
		QA: {
			id: state.widget_index,
			title: 'QA' + state.qa_index,
			type: 'QA',
			removable: true,
			expanded: true,
			maxHeight: '350px',
			maxWidth: '800px',
			text: ''
		},
		Timer: {
			id: state.widget_index,
			title: 'Timer',
			type: 'Timer',
			removable: true,
			expanded: true,
			maxHeight: '200px',
			maxWidth: '464px'
		},
		Pronunciation: {
			id: state.widget_index,
			title: 'Pronunciation difficulty',
			type: 'Pronunciation',
			removable: true,
			expanded: true,
			maxHeight: '250px',
			maxWidth: '800px',
			qa_id: 0
		}
	};
	return widget_templates[type];
}
