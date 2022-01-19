<template>
    <v-spacer>
        <v-container max-width="400" class="login">
            <v-img
                class="white--text align-end"
                height="200px"
                src="https://www.shopolog.ru/s/img/services/46/8b/800x400_468bc5dca58fbffcec2fff9785a48274___png____4_f90bca3e.png"
            >
            </v-img>
            <v-form>
                <v-container @click="bad_credentials = false">
                    <v-row>
                        <v-col
                        cols="12"
                        >
                        <v-text-field
                            v-model="username"
                            label="Логин"
                        ></v-text-field>

                        <v-text-field
                            v-model="password"
                            :type="show_password ? 'text' : 'password'"
                            label="Пароль"
                            @click:append="show_password = !show_password"
                        ></v-text-field>
                        </v-col>
                    </v-row>
                </v-container>
            </v-form>
            {{$store.state.token}}
            <div v-if='bad_credentials' class='red-text'>
                Неправильные данные для входа
            </div>
            <v-card-actions align="center">
                <v-btn 
                    color="orange" 
                    text 
                    @click="sendAuth()">
                    Войти
                </v-btn>
            </v-card-actions>
        </v-container>
    </v-spacer>
</template>

<script>
import axios from 'axios';

export default {

     data() {
         return {
             show_password: false,
             username: "",
             password: "",
             bad_credentials: false
         }
     },
     methods:{
        sendAuth(){
            const params = new URLSearchParams()
            params.append('username', this.username)
            params.append('password', this.password)
            axios.post(this.$store.state.host + "/api/token/", params).then(
                response => {
                    localStorage.setItem('token', response.data.access_token)
                    this.$store.state.token = response.data.access_token
                },
                error => {
                    if (error.response.status == 401){
                        this.bad_credentials = true
                    }
                }
            )
         }
     },
    created (){
        this.$store.state.token = localStorage.getItem('token');
    }
}
</script>

<style scoped>
.login {
    width: 400px;
    box-shadow: 0 0 20px 0 rgba(0, 0, 0, 0.2), 0 5px 5px 0 rgba(0, 0, 0, 0.24);
}
</style>