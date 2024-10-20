import Form from "../components/AuthenticationForm"
function Login(){
    return <Form route="/api/users/login" method="login"/>
}
 export default Login