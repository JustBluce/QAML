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
		questions: []
	},
	modules: {
		app,
		settings,
		user
	},
	mutations: {
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
		questions: (state) => state.questions,
		questions: (state) => (id) => state.questions.filter((question) => question.id === id)[0]
	}
});

export default store;
