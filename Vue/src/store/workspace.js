/**
 * Developers: Jason Liu
 */

export function defaultQA() {
	return {
		text: '',
		answer_text:'',
		country_representation: '',
		people_ethnicity: '',
		top5_similar_questions: [],
		binary_search_based_buzzer: '',
		importance: '',
		genre: '',
		subgenre: '',
		pronunciation:''
	};
}

export function widgetTemplate(id, type) {
	let widget_templates = {
		Timer: {
			id: id,
			title: 'Timer',
			type: 'Timer',
			container: 'left'
		},
		Pronunciation: {
			id: id,
			title: 'Pronunciation difficulty',
			type: 'Pronunciation',
			container: 'right'
		},
		CountryRepresentation: {
			id: id,
			title: 'Country representation',
			type: 'CountryRepresentation',
			container: 'right'
		},
		SimilarQuestions: {
			id: id,
			title: 'Similar questions',
			type: 'SimilarQuestions',
			container: 'right'
		},
		Buzzer: {
			id: id,
			title: 'Buzzer',
			type: 'Buzzer',
			container: 'left'
		},
		MachineGuesses: {
			id: id,
			title: 'Machine guesses',
			type: 'MachineGuesses',
			container: 'left'
		}
	};
	return widget_templates[type];
}

export function defaultWorkspace(id) {
	return {
		id: id,
		tab_id: id,
		tab: true,
		title: id === 0 ? 'Workspace' : `Workspace (${id})`,
		qa: defaultQA(),
		widgets: [
			widgetTemplate(0, 'Timer'),
			widgetTemplate(1, 'Pronunciation'),
			widgetTemplate(2, 'CountryRepresentation'),
			widgetTemplate(3, 'SimilarQuestions'),
			widgetTemplate(4, 'Buzzer'),
			widgetTemplate(5, 'MachineGuesses')
		],
		widget_index: 7,
		style: {
			left: 0,
			top: 0,
			width: 0,
			height: 0
		}
	};
}

export const initial_workspaces = [ defaultWorkspace(0) ];
