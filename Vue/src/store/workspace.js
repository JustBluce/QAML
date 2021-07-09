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
				top5_similar_questions: []
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
			},
			{
				id: 1,
				title: 'Representation',
				type: 'Representation',
				expanded: true,
				maxHeight: '400px'
			},
			{
				id: 2,
				title: 'Top 5 Similar Questions',
				type: 'SimilarQuestions',
				expanded: true,
				maxHeight: '400px'
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
		top5_similar_questions: []
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
		},
		SimilarQuestions: {
			id: workspace.widget_index,
			title: 'Top5 similar questions',
			type: 'SimilarQuestions',
			expanded: true,
			maxHeight: '300px',
		}
	};
	return widget_templates[type];
}
