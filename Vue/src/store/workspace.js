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
				top5_similar_questions: [],
				binary_search_based_buzzer:'',
				importance:'',
				genre: '',
				subgenre: ''
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
				maxHeight: '100px'
			},
			{
				id: 1,
				title: 'Pronunciation difficulty',
				type: 'Pronunciation',
				container: 'left',
				expanded: true,
				maxHeight: '200px',
			},
			{
				id: 3,
				title: 'Buzzer',
				type: 'Buzzer',
				container: 'left',
				expanded: true,
				maxHeight: '500px',
			},
			{
				id: 2,
				title: 'Suggestions',
				type: 'Representation',
				container: 'right',
				expanded: true,
				maxHeight: '300px',
			},
			{
				id: 4,
				title: 'Top 5 Similar Questions',
				type: 'SimilarQuestions',
				container: 'right',
				expanded: true,
				maxHeight: '400px'
			}
			
		],
		widget_index: 5
	};
}

export function defaultQA(id) {
	return {
		id: id,
		title: `QA (${id})`,
		text: '',
		country_representation: '',
		people_ethnicity: '',
		top5_similar_questions: [],
		binary_search_based_buzzer: '',
        importance:'',
		genre: '',
		subgenre: ''
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
			maxHeight: '100px',
		},
		Pronunciation: {
			id: workspace.widget_index,
			title: 'Pronunciation difficulty',
			type: 'Pronunciation',
			container: 'left',
			expanded: true,
			maxHeight: '200px',
		},
		Representation: {
			id: workspace.widget_index,
			title: 'Suggestions',
			type: 'Representation',
			container: 'right',
			expanded: true,
			maxHeight: '300px',
		},
		SimilarQuestions: {
			id: workspace.widget_index,
			title: 'Top5 similar questions',
			type: 'SimilarQuestions',
			expanded: true,
			maxHeight: '400px',
		},
		Buzzer: {
			id: workspace.widget_index,
			title: 'Buzzer',
			type: 'Buzzer',
			container: 'left',
			expanded: true,
			maxHeight: '500px',
		}
	};
	return widget_templates[type];
}
