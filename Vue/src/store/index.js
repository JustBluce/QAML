import Vue from 'vue';
import Vuex from 'vuex';
import * as getters from './getters';
import { defaultWorkspace, initial_workspaces, widgetTemplate } from './workspace';
import app from './modules/app';
import settings from './modules/settings';
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
			'SimilarQuestions',
			'MachineGuesses',
			'Buzzer',
			'Pronunciation',
			'CountryRepresentation'
		],
		game_mode: false,
		genreChartData: [ [ 'Genre', 'Count' ], [ 'None', 1 ] ],
		recommended: [ 'Baltimore', 'Washington, D.C.', 'Cleveland' ]
	},
	modules: {
		app,
		settings
	},
	mutations: {
		createWorkspace(state, title) {
			let newWorkspace = defaultWorkspace(state.workspace_index);
			if (title) {
				newWorkspace.title = title;
				state.recommended = state.recommended.filter((rec) => rec !== title);
			}
			state.workspaces.push(newWorkspace);
			state.workspace_index++;
			this.commit('updateTabs');
			this.commit('selectWorkspace', newWorkspace.id);
		},
		addWorkspace(state, workspace_id) {
			getters.workspace(state)(workspace_id).tab = true;
			this.commit('updateTabs');
			this.commit('selectWorkspace', workspace_id);
		},
		closeWorkspace(state, workspace_id) {
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
		resetWorkspace(state, workspace_id) {
			let workspace = getters.workspace(state)(workspace_id);
			let resetWorkspace = defaultWorkspace(0);
			workspace.qa = resetWorkspace.qa;
			workspace.widgets = resetWorkspace.widgets;
			workspace.results = resetWorkspace.results;
			workspace.style = resetWorkspace.style;
		},
		deleteWorkspace(state, workspace_id) {
			this.commit('closeWorkspace', workspace_id);
			state.workspaces = state.workspaces.filter((workspace) => workspace.id !== workspace_id);
			this.commit('updateTabs');
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
		addResult(state, { workspace_id, result }) {
			let workspace = getters.workspace(state)(workspace_id);
			workspace.results.dialog = true;
			workspace.results.content.push(result);
		},
		closeResults(state, workspace_id) {
			let workspace = getters.workspace(state)(workspace_id);
			workspace.results.dialog = false;
			workspace.results.content = [];
		}
	},
	getters: {
		//isLoggedIn: (state) => state.user.loggedIn,
		//userData: (state) => state.user.data,
		//verified: (state) => state.user.verified,

		sidebar: (state) => state.app.sidebar,
		device: (state) => state.app.device,
		//token: (state) => state.user.token,
		//avatar: (state) => state.user.avatar,
		//name: (state) => state.user.name,
		...getters
	},
	actions: {
		/* fetchUser({ commit }, user) {
			commit('SET_LOGGED_IN', user !== null);
			if (user) {
				commit('SET_USER', {
					displayName: user.displayName,
					email: user.email
				}),
				commit('SET_VERIFIED', {
					verified: user.emailVerified, 
				});
			} else {
				commit('SET_USER', null);
			}
		} */
	}
});

export default store;
