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
			container: 'right',
			expanded: true,
			maxHeight: '250px'
		},
		Country_Representation: {
			id: id,
			title: 'Country Representation',
			type: 'Country_Representation',
			container: 'right',
			expanded: true,
			maxHeight: '300px'
		},
		SimilarQuestions: {
			id: id,
			title: 'Similar questions',
			type: 'SimilarQuestions',
			expanded: true,
			container: 'right',
			maxHeight: '400px'
		},
		Buzzer: {
			id: id,
			title: 'Buzzer',
			type: 'Buzzer',
			container: 'left',
			expanded: true,
			maxHeight: '500px',
		},
		Machine_Guess: {
			id: id,
			title: 'Machine Guess',
			type: 'Machine_Guess',
			container: 'left',
			expanded: true,
			maxHeight: '500px'
		},
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
				binary_search_based_buzzer: '',
				importance: '',
				genre: '',
				subgenre: '',
				pronunication:'',
				answer:''
			}
		],
		qa_index: 1,
		qa_selected: 0,
		widgets: [
			widgetTemplate(0, 'Timer'),
			widgetTemplate(1, 'Pronunciation'),
			widgetTemplate(2, 'Country_Representation'),
			widgetTemplate(3, 'SimilarQuestions'),
			widgetTemplate(4, 'Buzzer'),
			widgetTemplate(5, 'Machine_Guess')
		],
		widget_index: 7,
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
		importance: '',
		genre: '',
		subgenre: '',
		pronunciation:'',
		answer:''
	}
}

export const initial_workspaces = [ defaultWorkspace(0) ];
