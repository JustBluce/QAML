import Vue from 'vue';
import Vuex from 'vuex';
import app from './modules/app';
import settings from './modules/settings';
import user from './modules/user';

Vue.use(Vuex);

const store = new Vuex.Store({
	state: {
		modal: {
			opened: false,
			difficulty: 'Easy',
			question_saved: false
		},
		widgets: [
			{
				id: '0',
				title: 'QA1',
				type: 'QA',
				removable: false,
				maxHeight: '350px'
			},
			{
				id: '1',
				title: 'QA2',
				type: 'QA',
				removable: true,
				maxHeight: '350px'
			},
			{
				id: '2',
				title: 'Timer',
				type: 'Timer',
				removable: true,
				maxHeight: '200px'
			},
			{
				id: '3',
				title: 'Pronunciation difficulty',
				type: 'Pronunciation',
				removable: true,
				maxHeight: '250px'
			}
		],
		questions: []
	},
	modules: {
		app,
		settings,
		user
	},
	mutations: {
		addWidget(state, widget) {
			state.widgets.push(widget);
		},
		deleteWidget(state, id) {
			state.widgets = state.widgets.filter((widget) => widget.id !== id);
		},
		addQuestion(state, id) {
			state.questions.push({
				id: id,
				text: ''
			});
		},
		updateQuestion(state, payload) {
			state.questions = state.questions.map(
				(question) => (question.id === payload.id ? { ...question, text: payload.text } : question)
			);
		}
	},
	getters: {
		sidebar: (state) => state.app.sidebar,
		device: (state) => state.app.device,
		token: (state) => state.user.token,
		avatar: (state) => state.user.avatar,
		name: (state) => state.user.name,
		questions: (state) => (id) => state.questions.filter((question) => question.id === id)[0]
	}
});

export default store;
