import Vue from 'vue';
import Vuex from 'vuex';
import * as getters from './getters';
import { defaultWorkspace, defaultQA, initial_workspaces, widgetTemplate } from './workspace';
import app from './modules/app';
import settings from './modules/settings';
import user from './modules/user';
import VueGoogleCharts from 'vue-google-charts';

Vue.use(VueGoogleCharts);
Vue.use(Vuex);

const store = new Vuex.Store({
	state: {
		workspaces: initial_workspaces,
		workspace_stack: initial_workspaces.map((workspace) => workspace.id),
		workspace_index: initial_workspaces.length,
		widget_types: [
			'Timer',
			'Pronunciation',
			'CountryRepresentation',
			'SimilarQuestions',
			'Buzzer',
			'MachineGuesses'
		],
		recommended: [ 'Baltimore', 'Washington, D.C.', 'Cleveland' ],
		results: {
			dialog: false,
			content: []
		}
	},
	modules: {
		app,
		settings,
		user
	},
	mutations: {
		addWorkspace(state, title) {
			let newWorkspace = defaultWorkspace(state.workspace_index);
			if (title) {
				newWorkspace.title = title;
			}
			state.workspaces.push(newWorkspace);
			state.workspace_stack.push(state.workspace_index);
			state.workspace_index++;
		},
		deleteWorkspace(state, workspace_id) {
			state.workspaces = state.workspaces.filter((workspace) => workspace.id !== workspace_id);
			state.workspace_stack = state.workspace_stack.filter((id) => id !== workspace_id);
		},
		selectWorkspace(state, workspace_id) {
			if (getters.workspace(state)(workspace_id)) {
				state.workspace_stack = state.workspace_stack.filter((id) => id !== workspace_id);
				state.workspace_stack.push(workspace_id);
			}
		},
		minimizeWorkspace(state, workspace_id) {
			state.workspace_stack = state.workspace_stack.filter((id) => id !== workspace_id);
		},
		addWidget(state, { workspace_id, type }) {
			let workspace = getters.workspace(state)(workspace_id);
			workspace.widgets.push(widgetTemplate(workspace.widget_index, type));
			workspace.widget_index++;
		},
		deleteWidget(state, { workspace_id, widget_id }) {
			let workspace = getters.workspace(state)(workspace_id);
			workspace.widgets = workspace.widgets.filter((widget) => widget.id !== widget_id);
		},
		createQA(state, workspace_id) {
			let workspace = getters.workspace(state)(workspace_id);
			workspace.qas.push(defaultQA(workspace.qa_index));
			workspace.qa_selected = workspace.qa_index;
			workspace.qa_index++;
			this.commit('updateQAs', workspace_id);
		},
		deleteQA(state, { workspace_id, qa_id }) {
			let workspace = getters.workspace(state)(workspace_id);
			workspace.qas = workspace.qas.filter((qa) => qa.id !== qa_id);
			workspace.qa_selected = workspace.qas[Math.min(workspace.qa_selected, workspace.qas.length - 1)].id;
			this.commit('updateQAs', workspace_id);
		},
		updateQAs(state, workspace_id) {
			let workspace = getters.workspace(state)(workspace_id);
			workspace.qa_selected = workspace.qas.findIndex((qa) => qa.id === workspace.qa_selected);
			workspace.qas = workspace.qas.map((qa, i) => Object.assign(qa, { id: i }));
		},
		addResult(state, result) {
			state.results.dialog = true;
			state.results.content.push(result);
		},
		closeResults(state) {
			state.results.dialog = false;
			state.results.content = [];
		}
	},
	getters: {
		sidebar: (state) => state.app.sidebar,
		device: (state) => state.app.device,
		token: (state) => state.user.token,
		avatar: (state) => state.user.avatar,
		name: (state) => state.user.name,
		...getters
	}
});

export default store;
