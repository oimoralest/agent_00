import { Button } from "@nextui-org/react";
import { Link } from "react-router-dom";

const Home = () => {
    return (
        <>
            <h1>Home</h1>
            <p>Welcome to the home page</p>
            <Button
                color="primary"
                className="p-0"
            >
                <Link to="/login" className="w-full h-full text-center m-auto flex justify-center items-center">Login</Link>
            </Button>
            <Button>
                <Link to="/register">Register</Link>
            </Button>
        </>
    )
}

export default Home;
