export function defaultQA(id) {
	return {
		id: id,
		title: id === 0 ? 'QA' : `QA (${id})`,
		text: '',
		answer:'',
		country_representation: '',
		people_ethnicity: '',
		top5_similar_questions: [],
		binary_search_based_buzzer: '',
		importance: '',
		genre: '',
		subgenre: ''
	};
}

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
			title: 'Speech To Text Transcription',
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
		title: id === 0 ? 'Workspace' : `Workspace (${id})`,
		qas: [ defaultQA(0) ],
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

export const initial_workspaces = [ defaultWorkspace(0) ];
