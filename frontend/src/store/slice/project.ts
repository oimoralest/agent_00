import { createSlice } from "@reduxjs/toolkit";

const Project = createSlice({
  name: "project",
  initialState: {
    id: null,
    name: null,
    agents: [],
  },
  reducers: {
    setProject: (state, action) => {
      state.id = action.payload.id;
      state.name = action.payload.name;
      state.agents = action.payload.agents;
    },
    getProject: (state) => {
      return state;
    },
  },
});

export const { setProject, getProject } = Project.actions;
export default Project.reducer;

export const fetchProject = (projectId: string) => async (dispatch: any, getState: any) => {
  try {
    const response = await fetch(`http://localhost:8000/api/v1/project?id=${projectId}`);
    const project = await response.json();
    dispatch(setProject(project));
  } catch (error) {
    // TODO : Modal alert
    console.log(error);
  }
};

export const createProject = (project: any) => async (dispatch: any, getState: any) => {
  try {
    const response = await fetch(`http://localhost:8000/project`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(project),
    });
    const projectResponse = await response.json();
    if (response.status !== 200) throw new Error(projectResponse.message);
    window.location.href = `/project/${projectResponse.id}`;
  } catch (error) {
    // TODO : Modal alert
    console.log(error);
  }
}

export const loginProject = (project: any) => async (dispatch: any, getState: any) => {
  try {
    const response = await fetch(`http://localhost:8000/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(project),
    });
    const projectResponse = await response.json();
    if (response.status !== 200) throw new Error(projectResponse.message);
    window.location.href = `/project/${projectResponse.id}`;
  } catch (error) {
    // TODO : Modal alert
    console.log(error);
  }
}

