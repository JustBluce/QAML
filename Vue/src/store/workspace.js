/**
 * Developers: Jason Liu
 */

export const widget_types = [
    'Timer',
    'MachineGuesses',
    'SimilarQuestions',
    'Buzzer',
    'Pronunciation',
    'CountryRepresentation',
    'EntityRepresentation'
];

const default_widgets = [
    {
        id: 0,
        show: 0,
        title: 'Timer',
        type: 'Timer',
        container: 'left',
        info: 'Timer for game mode'
    },
    {
        id: 1,
        show: 1,
        title: 'Machine guesses',
        type: 'MachineGuesses',
        container: 'left',
        info: 'List of top machine guesses w/ confidence scores'
    },
    {
        id: 2,
        show: 1,
        title: 'Similar questions',
        type: 'SimilarQuestions',
        container: 'left',
        info: 'List of past questions the AI finds similar to yours'
    },
    {
        id: 3,
        show: 1,
        title: 'Buzzer',
        type: 'Buzzer',
        container: 'right',
        info: 'Buzzer text w/ buzz position highlighting and sentence importance scores'
    },
    {
        id: 4,
        show: 1,
        title: 'Pronunciation difficulty',
        type: 'Pronunciation',
        container: 'right',
        info: 'List of words that are suggested to have a pronunciation guide'
    },
    {
        id: 5,
        show: 1,
        title: 'Country representation',
        type: 'CountryRepresentation',
        container: 'right',
        info: 'List of suggested underrepresented countries related to your question'
    },
    {
        id: 6,
        show: 1,
        title: 'Entity representation',
        type: 'EntityRepresentation',
        container: 'right',
        info: 'List of suggested underrepresented answer entities related to your question'
    }
];

export function defaultQA() {
    return {
        text: '',
        answer: [],
        answer_text: '',
        country_representation: [],
        entity_representation: [],
        people_ethnicity: '',
        top5_similar_questions: [],
        binary_search_based_buzzer: 'Buzzer text goes here',
        importance: [],
        genre: '',
        subgenre: {},
        top_guess_buzzer: '',
        uid: '',
        pronunciation: [],
        buzz_word_this: '',
        highlight_words: {}
    };
}

export function defaultWorkspace(id) {
    return {
        id: id,
        tab_id: id + 1,
        tab: true,
        title: id === 0 ? 'Workspace' : `Workspace (${id})`,
        qa: defaultQA(),
        widgets: default_widgets.map((widget) => {
            return { ...widget };
        }),
        widget_timestamps: widget_types.reduce((ac, a) => ({ ...ac, [a]: Date.now() }), {}),
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
