import { createSlice } from "@reduxjs/toolkit";


const Agent = createSlice({
  name: "agent",
  initialState: {
    id: null,
    name: null,
    description: null,
    project_id: null,
    nodes: [],
  },
  reducers: {
    setAgent: (state, action) => {
      console.log("setAgent", action.payload)
      state.id = action.payload.id;
      state.name = action.payload.name;
      state.project_id = action.payload.project_id;
      state.nodes = action.payload.nodes;
    },
    getAgent: (state) => {
      return state;
    },
    appendNode: (state, action) => {
      state.nodes.push(action.payload);
    }
  },
});

export const { setAgent, getAgent, appendNode } = Agent.actions;
export default Agent.reducer;

export const fetchAgent = (agentId: string) => async (dispatch: any, getState: any) => {
  try {
    const response = await fetch(`http://localhost:8000/api/v1/agent?id=${agentId}`);
    const agents = await response.json();
    dispatch(setAgent(agents));
  } catch (error) {
    // TODO : Modal alert
    console.log(error);
  }
};

export const createAgent = (agent: any) => async (dispatch: any, getState: any) => {
  try {
    console.log(agent);
    const response = await fetch(`http://localhost:8000/api/v1/agent`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(agent),
    });
    const agentResponse = await response.json();
    if (response.status !== 201) throw new Error(agentResponse.message);
    dispatch(setAgent(agentResponse));
    window.location.href = `/agent/${agentResponse.id}`;
  } catch (error) {
    // TODO : Modal alert
    console.log(error);
  }
}
