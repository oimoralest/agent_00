import { createSlice } from "@reduxjs/toolkit";
import { appendNode } from "./agent";


const Node = createSlice({
  name: "node",
  initialState: {
    id: null,
    agent_id: null,
    type: null,
    data: {},
  },
  reducers: {
    setNode: (state, action) => {
      state.id = action.payload.id;
      state.agent_id = action.payload.agent_id;
      state.type = action.payload.type;
      state.data = action.payload.data;
    },
    getNode: (state) => {
      return state;
    }
  },
});

export const { setNode, getNode } = Node.actions;
export default Node.reducer;

export const createNode = (node: any) => async (dispatch: any, getState: any) => {
  try {
    const response = await fetch(`http://localhost:8000/api/v1/node`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(node),
    });
    const nodeResponse = await response.json();
    if (response.status !== 201) throw new Error(nodeResponse.message);
    dispatch(setNode(nodeResponse));
    dispatch(appendNode(nodeResponse));
  } catch (error) {
    // TODO : Modal alert
    console.log(error);
  }
}
