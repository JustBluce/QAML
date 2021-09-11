/**
 * Developers: Jason Liu
 */

export function widgetTemplate(type) {
	let widget_templates = {
		Timer: {
			id: 0,
			title: 'Timer',
			type: 'Timer',
			container: 'left'
		},
		MachineGuesses: {
			id: 1,
			title: 'Machine guesses',
			type: 'MachineGuesses',
			container: 'left'
		},
		SimilarQuestions: {
			id: 2,
			title: 'Similar questions',
			type: 'SimilarQuestions',
			container: 'left'
		},
		Buzzer: {
			id: 3,
			title: 'Buzzer',
			type: 'Buzzer',
			container: 'right'
		},
		Pronunciation: {
			id: 4,
			title: 'Pronunciation difficulty',
			type: 'Pronunciation',
			container: 'right'
		},
		CountryRepresentation: {
			id: 5,
			title: 'Country representation',
			type: 'CountryRepresentation',
			container: 'right'
		}
	};
	return widget_templates[type];
}

export function defaultQA() {
	return {
		text: '',
		answer: [],
		answer_text: '',
		country_representation: [],
		people_ethnicity: '',
		top5_similar_questions: [],
		binary_search_based_buzzer: 'Buzzer text goes here',
		importance: [],
		genre: '',
		subgenre: '',
		top_guess_buzzer: '',
		uid:'',
		pronunciation: [],
		buzz_word_this:'',
		highlight_words : {},
	};
}

export function defaultWorkspace(id) {
	return {
		id: id,
		tab_id: id + 1,
		tab: true,
		title: id === 0 ? 'Workspace' : `Workspace (${id})`,
		qa: defaultQA(),
		widgets: [
			widgetTemplate('Timer'),
			widgetTemplate('SimilarQuestions'),
			widgetTemplate('MachineGuesses'),
			widgetTemplate('Buzzer'),
			widgetTemplate('Pronunciation'),
			widgetTemplate('CountryRepresentation')
		],
		results: {
			dialog: false,
			content: []
		},
		style: {
			left: 0,
			top: 0,
			width: 0,
			height: 0
		}
	};
}

export const initial_workspaces = [ defaultWorkspace(0) ];