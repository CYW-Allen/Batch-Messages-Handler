<template>
  <q-dialog v-model="appStatus.displayModifyColDlg" @before-hide="curModifyType = 'create'" persistent>
    <q-card style="width: 50vw">
      <q-card-section class="row justify-start items-center">
        <div class="text-h6 text-bold q-mr-md">Modify type</div>
        <q-option-group class="text-subtitle1" size="md" inline v-model="curModifyType" :options="modifyTypeOpts"
          @update:model-value="resetModifyCol" />
      </q-card-section>

      <q-separator inset />

      <q-card-section class="scroll q-mb-md" style="max-height: 70vh;">
        <q-tab-panels v-model="curModifyType" animated>
          <q-tab-panel name="create">
            <q-input type="text" bg-color="blue-1" standout="bg-blue-3" class="q-mb-sm" input-class="text-h6"
              v-for="index in modifications.length" :key="`newCol${index}`" v-model="modifications[index - 1]">
              <template v-slot:prepend>
                <div class="text-h6 text-blue-10 text-bold">Column name :</div>
              </template>
              <template v-slot:append>
                <q-icon name="fa-solid fa-eraser" class="cursor-pointer q-mr-sm" @click="modifications[index - 1] = ''" />
                <q-icon name="fa-solid fa-trash-can" class="cursor-pointer" @click="modifications.splice(index - 1, 1)" />
              </template>
            </q-input>
          </q-tab-panel>
          <q-tab-panel name="remove">
            <q-select class="text-subtitle1 q-mb-sm" filled multiple v-model="modifications" :options="colList">
              <template v-slot:prepend>
                <div class="text-h6 text-blue-10 text-bold">Remove column :</div>
              </template>
              <template v-slot:selected-item="scope">
                <q-chip class="glossy" color="blue-8" text-color="white" removable :tabindex="scope.tabindex"
                  @remove="scope.removeAtIndex(scope.index)">
                  {{ scope.opt }}
                </q-chip>
              </template>
            </q-select>
          </q-tab-panel>
        </q-tab-panels>
      </q-card-section>

      <q-card-actions align="between">
        <q-btn v-if="curModifyType === 'create'" glossy push size="md" color="positive" label="New column"
          @click="modifications.push('')" />
        <div v-else></div>
        <q-btn-group glossy>
          <q-btn label="Cancel" color="grey" push v-close-popup no-caps />
          <q-btn label="Confirm" color="primary" push v-close-popup no-caps @click="processModify"
            :disable="modifications.length === 0" />
        </q-btn-group>
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup>
import { computed, ref } from 'vue';
import { useAppStatusStore } from 'src/stores/appStatus';

const appStatus = useAppStatusStore();

const emit = defineEmits(['updateColOptions']);

const colList = computed(() => Object.keys(appStatus.mails[0] || {}).filter((col) => col !== 'Index'));
const modifyTypeOpts = [
  { label: 'Create column', value: 'create' },
  { label: 'Remove column', value: 'remove' },
];
const curModifyType = ref('create');
const modifications = ref(['']);

function resetModifyCol(type) {
  if (type === 'create') modifications.value = [''];
  else modifications.value = [];
}

function processModify() {
  if (curModifyType.value === 'create') {
    appStatus.mails[0] = {
      ...appStatus.mails[0],
      ...modifications.value.filter((col) => col !== '').reduce((result, col) => {
        result[col] = '';
        return result;
      }, {}),
    };
  } else {
    const cols = Object.keys(appStatus.mails[0]);

    modifications.value.forEach((col) => {
      appStatus.mails.forEach((mail) => { delete mail[col]; });
      emit('updateColOptions', cols.indexOf(col));
    });
  }
}
</script>
