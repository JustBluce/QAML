/**
 * Developers: Jason Liu
 */

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
		pronunciation: []
	};
}

export function widgetTemplate(type) {
	let widget_templates = {
		Timer: {
			id: 0,
			title: 'Timer',
			type: 'Timer',
			container: 'left'
		},
		Pronunciation: {
			id: 1,
			title: 'Pronunciation difficulty',
			type: 'Pronunciation',
			container: 'right'
		},
		CountryRepresentation: {
			id: 2,
			title: 'Country representation',
			type: 'CountryRepresentation',
			container: 'right'
		},
		SimilarQuestions: {
			id: 3,
			title: 'Similar questions',
			type: 'SimilarQuestions',
			container: 'right'
		},
		Buzzer: {
			id: 4,
			title: 'Buzzer',
			type: 'Buzzer',
			container: 'left'
		},
		MachineGuesses: {
			id: 5,
			title: 'Machine guesses',
			type: 'MachineGuesses',
			container: 'left'
		},
	};
	return widget_templates[type];
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
			widgetTemplate('Pronunciation'),
			widgetTemplate('CountryRepresentation'),
			widgetTemplate('SimilarQuestions'),
			widgetTemplate('Buzzer'),
			widgetTemplate('MachineGuesses')
		],
		style: {
			left: 0,
			top: 0,
			width: 0,
			height: 0
		}
	};
}

export const initial_workspaces = [ defaultWorkspace(0) ];
