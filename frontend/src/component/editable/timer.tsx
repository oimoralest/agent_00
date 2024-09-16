import {
    ModalHeader,
    ModalBody,
    Input,
    ModalFooter,
    Button,
} from "@nextui-org/react";
import { useDispatch, useSelector } from "react-redux";
import { createNode } from "../../store/slice/node";

const Timer = () => {
    const agent = useSelector((state: any) => state.agent);
    const dispatch = useDispatch();

    return (
        <>
            <ModalHeader>Timer</ModalHeader>
            <ModalBody>
                <Input
                    id="timerName"
                    type="number"
                    label="time"
                    min={1}
                    max={60}
                ></Input>
            </ModalBody>
            <ModalFooter>
                <Button
                    color="primary"
                    onPress={() => {
                        const timerInput = document.getElementById("timerName") as HTMLInputElement;
                        dispatch(createNode(
                            {
                                id: null,
                                type: "timer",
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

export default Timer;