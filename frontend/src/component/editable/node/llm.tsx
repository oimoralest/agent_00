import {
  ModalHeader,
  ModalBody,
  Input,
  ModalFooter,
  Button,
  Select,
  SelectItem,
  Divider,
  Slider,
  Tab,
  Tabs,
  Card,
  CardBody,
  Textarea
} from "@nextui-org/react";
import { useState } from "react"
import { useDispatch, useSelector } from "react-redux";
import { createNode } from "../../../store/slice/node";

const LLM = () => {
  const agent = useSelector((state: any) => state.agent);
  const dispatch = useDispatch();

  const [selectedProvider, setSelectedProvider] = useState(new Set([]));
  const [selectedModel, setSelectedModel] = useState(new Set([]));
  const [selectedTemperature, setSelectedTemperature] = useState(0.5);

  // TODO: Place this in a shared file or fetch from the API?
  const modelsMapper = {
    "Open AI": ["gpt-3", "gpt-4", "gpt-4o"],
  }

  return (
    <>
      <ModalHeader>LLM</ModalHeader>
      <ModalBody>
        <Input
          id="llmName"
          type="text"
          label="LLM Name"
          isRequired={true}
        ></Input>
        <Input
          id="llmDescription"
          type="text"
          label="Description"
        ></Input>
        <Tabs aria-label="LLM settings" disableAnimation={true}>
          <Tab key="provider" title="Provider" className="flex flex-col w-full gap-2">
            <Select
              label="Provider"
              placeholder="Select a provider"
              selectionMode="single"
              onSelect={(e) => console.log(e)}
              selectedKeys={selectedProvider}
              onSelectionChange={setSelectedProvider}
              isRequired={true}
            >
              {Object.keys(modelsMapper).map((provider) => {
                return (
                  <SelectItem key={provider} value={provider}>{provider}</SelectItem>
                )
              })}
            </Select>
            <Select
              label="Model"
              placeholder="Select a model"
              selectionMode="single"
              onSelect={(e) => console.log("On select", e)}
              selectedKeys={selectedModel}
              onSelectionChange={setSelectedModel}
              isRequired={true}
            >
              {selectedProvider.size && modelsMapper[selectedProvider.values().next().value].map((model) => {
                return (
                  <SelectItem key={model} value={model}>{model}</SelectItem>
                )
              })}
            </Select>

          </Tab>
          <Tab key="settings" title="Model settings" className="flex flex-col w-full gap-2">
            <Textarea label="Prompt" placeholder="Type your prompt" />
            <Slider
              label="Temperature"
              minValue={0}
              maxValue={1}
              step={0.1}
              defaultValue={0.5}
              onChangeEnd={(e) => setSelectedTemperature(e)}
            />
          </Tab>
        </Tabs>
      </ModalBody >
      <ModalFooter>
        <Button
          color="primary"
          onPress={() => {
            const timerInput = document.getElementById("timerName") as HTMLInputElement;
            dispatch(createNode(
              {
                id: null,
                type: "llm",
                agent_id: agent.id,
                data: {
                  time: timerInput.value
                },
              }
            ));
          }}
        >Save</Button>
      </ModalFooter>
    </>
  )
}

export default LLM;
