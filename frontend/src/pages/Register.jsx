import Form from "../components/AuthenticationForm"

function Register() {
    return <Form route="/api/users/register" method="register" />
}

export default Register