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
		},
		SimilarQuestions: {
			id: id,
			title: 'Top5 similar questions',
			type: 'SimilarQuestions',
			expanded: true,
			container: 'right',
			maxHeight: '400px',
		},
		Buzzer: {
			id: id,
			title: 'Buzzer',
			type: 'Buzzer',
			container: 'left',
			expanded: true,
			maxHeight: '500px',
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
		
			widgetTemplate(0, 'Timer'),
			widgetTemplate(1, 'Pronunciation'),
			widgetTemplate(2, 'Representation'),
			widgetTemplate(3, 'SimilarQuestions'),
			widgetTemplate(4, 'Buzzer')
		],
		widget_index: 5,
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
		people_ethnicity: '',
		top5_similar_questions: [],
		binary_search_based_buzzer: '',
        importance:'',
		genre: '',
		subgenre: ''
	}
}

export const initial_workspaces = [ defaultWorkspace(0) ];

