<template>
    <div>
        <div class="header-menu">
            <v-row>
                <v-col cols=3>
                    <v-row>
                        <v-text-field
                            v-model="rnm"
                            label="Регистрационный номер"
                            clearable
                            clear-icon="close"/>
                        <v-btn
                            color="orange"
                            @click=getRNM()>
                            <v-icon>search</v-icon>
                        </v-btn> 
                    </v-row>
                </v-col>
                
                <v-col cols=3>
                    <v-row>
                        <v-text-field
                            v-model="fn"
                            label="Фискальный накопитель"
                            clearable
                            clear-icon="close"/>
                        <v-btn
                            color="orange"  
                            @click=getFN()>
                            <v-icon>search</v-icon>
                        </v-btn>
                    </v-row>
                </v-col>

                <v-col cols=3>
                    <v-row>
                        <v-text-field
                            v-model="zn"
                            label="Заводской номер"
                            clearable
                            clear-icon="close"/>
                        <v-btn
                            color="orange"
                            @click=getZN()>
                            <v-icon>search</v-icon>
                        </v-btn>

                        <v-col cols=1>
                            <v-btn 
                                x small
                                color="black"
                                @click=clearTable()
                                >
                                Очистить
                            </v-btn>
                        </v-col>
                    </v-row>
                </v-col>
            </v-row>
        </div>

        <v-simple-table>
            <template v-slot:default>
                <thead>
                <tr>
                    <th>
                    Регистрационны номер	
                    </th>
                    <th>
                    Номер фискльного накопителя	
                    </th>
                    <th>
                    Заводской номер	
                    </th>
                    <th>
                    Техническая блокировка	
                    </th>
                    <th>
                    Финансовая блокировка	
                    </th>
                    <th>
                    Дата начала обслуживания	
                    </th>
                    <th>
                    Дата окончания обслуживания
                    </th>
                </tr>
                </thead>
                <tbody>
                <tr
                    v-for="item in items"
                    :key="item.name"
                >
                    <td>{{ item.register_number_kkt }}</td>
                    <td>{{ item.factory_number_fn }}</td>
                    <td>{{ item.factory_number_kkt }}</td>
                    <td>{{ item.activated }}</td>
                    <td>{{ item.locked_no_payment }}</td>
                    <td>{{ item.start_date }}</td>
                    <td>{{ item.end_date }}</td>
                    <td>
                    <div v-for="item in item.items" :key=item>
                        {{ item }}
                    </div>
                    </td>
                </tr>
                </tbody>
            </template>
        </v-simple-table>
    <div/>
    <div v-if="show_error" class="red-text">ККТ не найдена. Измените поисковой запрос.</div>

  </div>
</template>

<script>
  import axios from 'axios';

  export default {
    data () {
      return {
        rnm: "",
        fn: "",
        zn: "",
        items: [],
        show_error: false
      }
    },
    methods:{
            processResponse(response){
                    this.items = response.data
                    if (this.items.length == 0){
                      this.show_error = true
                    }
                    else {
                      this.show_error = false
                    } 
            },
            getRNM(){
              let headers = {headers: {Authorization: "Bearer " + this.$store.state.token}}
              axios.get(this.$store.state.host + "/api/users/kkt/rnm/" + this.rnm, headers).then(
                response => this.processResponse(response))
            },
            getFN(){
              let headers = {headers: {Authorization: "Bearer " + this.$store.state.token}}
              axios.get(this.$store.state.host + "/api/users/kkt/fn/" + this.fn, headers).then(
                response => this.processResponse(response))
            },
            getZN(){
              let headers = {headers: {Authorization: "Bearer " + this.$store.state.token}}
              axios.get(this.$store.state.host + "/api/users/kkt/zn/" + this.zn, headers).then(
                response => this.processResponse(response))
            },
            clearTable(){
              this.show_error = false,
              this.items = []
            }
    }
}
</script>