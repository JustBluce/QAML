import Vue from 'vue';
import Vuex from 'vuex';
import * as getters from './getters';
import { defaultWorkspace, initial_workspaces, widgetTemplate } from './workspace';
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
		workspace_selected: initial_workspaces[0].tab_id,
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
		createWorkspace(state, title) {
			let newWorkspace = defaultWorkspace(state.workspace_index);
			if (title) {
				newWorkspace.title = title;
				state.recommended = state.recommended.filter((rec) => rec !== title);
			}
			state.workspaces.push(newWorkspace);
			state.workspace_stack.push(state.workspace_index);
			state.workspace_selected = state.workspace_index + 1;
			state.workspace_index++;
			this.commit('updateTabs');
		},
		removeWorkspace(state, workspace_id) {
			this.commit('minimizeWorkspace', workspace_id);
			getters.workspace(state)(workspace_id).tab = false;
		},
		selectWorkspace(state, workspace_id) {
			state.workspace_stack = state.workspace_stack.filter((id) => id !== workspace_id);
			state.workspace_stack.push(workspace_id);
			state.workspace_selected = getters.workspace(state)(workspace_id).tab_id;
		},
		minimizeWorkspace(state, workspace_id) {
			state.workspace_stack = state.workspace_stack.filter((id) => id !== workspace_id);
			if (state.workspace_stack.length > 0) {
				state.workspace_selected = getters.workspace(state)(state.workspace_stack.slice(-1)[0]).tab_id;
			} else {
				state.workspace_selected = 0;
			}
		},
		updateTabs(state) {
			state.workspace_selected =
				state.workspaces.findIndex((workspace) => workspace.tab_id === state.workspace_selected) + 1;
			state.workspaces = state.workspaces.map((workspace, i) => Object.assign(workspace, { tab_id: i + 1 }));
		},
		addWidget(state, { workspace_id, type }) {
			let workspace = getters.workspace(state)(workspace_id);
			if (!workspace.widgets.find((widget) => widget.type === type)) {
				workspace.widgets.push(widgetTemplate(type));
			}
		},
		deleteWidget(state, { workspace_id, type }) {
			let workspace = getters.workspace(state)(workspace_id);
			workspace.widgets = workspace.widgets.filter((widget) => widget.type !== type);
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
