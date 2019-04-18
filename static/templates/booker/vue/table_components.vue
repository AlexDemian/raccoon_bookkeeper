Vue.component('table-row', {

        props: {
            'act': Object,
            'pk': Number
        },


        data: function () {
            return {}
        },

        template: `<tr>
            <td><input type="image" :src="'/img/booker/' + [ act.active ? 'pinned' : 'unpinned' ] + '.png' " class='pin-button' @click='activate_row();' style='width: 20px; height: 20px;'></td>
            <td><input :value ='[[ act.name ]]' class="table-edit-field"></td>
            <td><input :value ='[[ act.descr ]]' class="table-edit-field"></td>
            <td>[[ act.category ]]</td>
            <td><input :value ='[[ act.value ]]' class="table-edit-field"></td>
            <td>
                <button class="btn btn-danger btn-sm" type="button" @click="delete_row();">X</button>
            </td>
            </tr>`

});

Vue.component('table-row-total', {

    props: {
        'costs': Number,
        'earnings': Number
    },

    data: function (){
        return {
            delta: this.costs + this.earnings,
            color: 'font-color: red',
            positive: 'font-color: green'

        }
    },

    template: `<tr class="tr-total">
        <td>Total:</td>
        <td>Earnings: [[ earnings ]]</td>
        <td>Costs: [[ costs ]]</td>
        <td :class="[ delta < 0 ? 'font-red' : 'font-green' ]">Delta: [[ delta ]]</td>
        <td></td>
        <td></td>
        </tr>`

});
