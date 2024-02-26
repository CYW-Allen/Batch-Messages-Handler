<template>
  <q-dialog v-model="appStatus.displayModifyRowDlg" @show="resetConfig" persistent>
    <q-card style="width: 80vw; max-width: 80vw;">
      <q-card-section class="row justify-start items-center">
        <div class="text-h5 text-bold q-mr-md">Modify type</div>
        <q-option-group class="text-subtitle1" v-model="curModifyType" size="md" inline :options="modifyTypeOpts"
          @update:model-value="resetConfig" />
      </q-card-section>

      <q-separator inset />

      <q-card-section>
        <q-tab-panels class="newRowPanels" v-model="curModifyType" animated>
          <q-tab-panel name="create">
            <div class="row" style="border-bottom: 2px solid lightgrey;">
              <div v-for="col, index in colList" :key="`row-col-${index}`"
                :class="`col row justify-center items-center q-pa-xs ${index % 2 === 0 ? 'bg-light-blue-3' : 'bg-light-blue-1'}`">
                <q-select v-if="col === 'Index'" class="text-h6" square dense v-model="curAddNum" bg-color="transparent"
                  borderless :options="addNumOpts" @update:model-value="addNewRows">
                  <template v-slot:prepend>
                    <div class="text-h6 text-weight-bold">Add rows: </div>
                  </template>
                </q-select>
                <div v-else class="text-h6 text-bold q-mr-sm">{{ col }}</div>
                <q-icon v-if="col !== 'Index'" class="cursor-pointer q-pt-xs" size="xs" name="fa-regular fa-pen-to-square"
                  @click="reqFillEntireCol(col)" />
              </div>
            </div>
            <q-scroll-area class="rowSelectScrollArea" style="height: 55vh;" id="newRowsField">
              <q-virtual-scroll scroll-target="#newRowsField > .scroll" :items="modification" separator
                v-slot="{ item, index }" @click="editCell">
                <q-item :key="index" class="row q-pa-none" dense>
                  <div v-for="col, colNum in Object.keys(item)" :key="`row-${index}-${col}`"
                    :class="`col cursor-pointer ${colNum % 2 === 0 ? 'bg-light-blue-3' : 'bg-light-blue-1'}`" square
                    :data-col="`${index}-${col}`" dense filled>
                    <div :class="`full-width text-center text-h6 ellipsis`" :data-col="`${index}-${col}`">{{ item[col] }}
                    </div>
                  </div>
                </q-item>
              </q-virtual-scroll>
            </q-scroll-area>
          </q-tab-panel>

          <q-tab-panel name="remove">
            <div v-if="appStatus.selectedRows.length === 0" class="text-h6 text-bold text-negative">First select unwanted
              rows</div>
            <div v-else>
              <div class="row" style="border-bottom: 2px solid lightgrey">
                <div v-for="col, colIndex in colList" :key="`row-col-${colIndex}`"
                  :class="`col text-center text-h6 text-bold ${colIndex % 2 === 0 ? 'bg-light-blue-3' : 'bg-light-blue-1'}`">
                  {{ col }}
                </div>
              </div>
              <q-scroll-area class="rowSelectScrollArea" style="height: 55vh;" id="deleteRowSelection" visible>
                <q-virtual-scroll scroll-target="#deleteRowSelection > .scroll" :items="appStatus.selectedRows.slice()"
                  separator v-slot="{ item, index }" @click="viewCellContent">
                  <q-item :key="index" class="row q-pa-none" dense>
                    <div v-for="col, colNum in Object.keys(item)" :key="`cell-${col}`"
                      :class="`dataCell col cursor-pointer text-center vertical-middle q-px-sm text-h6 ellipsis ${colNum % 2 === 0 ? 'bg-light-blue-3' : 'bg-light-blue-1'}`">
                      {{ item[col] }}
                    </div>
                  </q-item>
                </q-virtual-scroll>
              </q-scroll-area>
            </div>
          </q-tab-panel>
        </q-tab-panels>
      </q-card-section>

      <q-card-actions align="right">
        <q-btn-group glossy push>
          <q-btn label="Cancel" color="grey" v-close-popup no-caps />
          <q-btn label="Confirm" color="primary" v-close-popup @click="processRowEditions" no-caps
            :disable="(curModifyType === 'create' && modification.length === 0) || (curModifyType === 'remove' && appStatus.selectedRows.length === 0)" />
        </q-btn-group>
      </q-card-actions>
    </q-card>
  </q-dialog>

  <q-dialog v-model="displayViewCellDlg">
    <q-card style="width: 50vw; max-width: 50vw;">
      <q-card-section class="row justify-center items-center q-pa-sm" style="height: 50vh;">
        <q-scroll-area style="width: 100%; height: 100%;">
          {{ curCellContent }}
        </q-scroll-area>
      </q-card-section>

      <q-card-actions align="center">
        <q-btn glossy push label="Close" color="grey" v-close-popup no-caps />
      </q-card-actions>
    </q-card>
  </q-dialog>

  <q-dialog v-model="displayEditCellDlg" persistent>
    <q-card style="width: 50vw; max-width: 50vw;">
      <q-card-section>
        <div class="text-h5 text-bold q-mr-md">Cell at {{ `row ${curEditIndex.row}, col ${curEditIndex.col}` }}</div>
      </q-card-section>

      <q-card-section class="q-pa-sm" style="height: 50vh;">
        <q-input class="col rowDataTextarea" v-model="modification[curEditIndex.row][curEditIndex.col]" filled
          type="textarea" input-class="text-subtitle1" autofocus input-style="resize:none;height:100%"
          bg-color="light-blue-1" />
      </q-card-section>

      <q-card-actions align="right">
        <q-btn glossy push label="Cancel" color="grey" v-close-popup no-caps />
        <q-btn glossy push label="Confirm" color="primary" v-close-popup no-caps />
      </q-card-actions>
    </q-card>
  </q-dialog>

  <q-dialog v-model="displayEditColDlg">
    <q-card style="width: 50vw; max-width: 50vw;">
      <q-card-section>
        <div class="text-h5 text-bold q-mr-md">Fill entire column {{ curEditCol }}</div>
      </q-card-section>

      <q-card-section class="q-pa-sm scroll" style="height: 70vh;max-height: 70vh;">
        <div class="fit column">
          <div class="text-subtitle1 text-bold text-negative text-italic q-pa-none">
            One line content will be treated as one cell data ex:<br>
            <span class="q-ml-md">111</span><br>
            <span class="q-ml-md">222</span><br>
            There are two cell data. * The rest of cell will be filled with the last data(ex: 222)
          </div>
          <q-input class="col rowDataTextarea" v-model="batchCellNewContent" filled type="textarea"
            input-class="text-subtitle1" autofocus input-style="resize:none;" bg-color="light-blue-1" wrap="off" />
        </div>
      </q-card-section>

      <q-card-actions align="right">
        <q-btn glossy push label="Cancel" color="grey" v-close-popup no-caps />
        <q-btn glossy push label="Confirm" color="primary" v-close-popup no-caps @click="fillEntireCol" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup>
import { computed, nextTick, ref } from 'vue';
import { useQuasar } from 'quasar';
import { useAppStatusStore } from 'src/stores/appStatus';

const $q = useQuasar();
const appStatus = useAppStatusStore();

const modifyTypeOpts = [
  { label: 'Create row', value: 'create' },
  { label: 'Remove row', value: 'remove' },
];
const curModifyType = ref('create');
const addNumOpts = ref(Array.from({ length: 100 }, (_, i) => i + 1));
const curAddNum = ref(1);
const modification = ref([]);
const curEditCol = ref(null);
const curEditIndex = ref(null);
const displayEditCellDlg = ref(false);
const displayViewCellDlg = ref(false);
const curCellContent = ref(null);
const displayEditColDlg = ref(false);
const batchCellNewContent = ref('');

const colList = computed(() => Object.keys(appStatus.mails[0] || {}));

function getNewRow(index) {
  return colList.value.reduce((row, col) => {
    row[col] = col === 'Index' ? index : '';
    return row;
  }, {});
}

function resetConfig() {
  curAddNum.value = 1;
  modification.value = [getNewRow(appStatus.mails.length + 1)];
}

function addNewRows() {
  modification.value = Array.from({ length: curAddNum.value }, (_, index) => getNewRow(appStatus.mails.length + index + 1));
}

function reqFillEntireCol(col) {
  curEditCol.value = col;
  displayEditColDlg.value = true;
}

function editCell(event) {
  const [row, col] = event.target.dataset.col.split('-');

  curEditIndex.value = { row, col };
  displayEditCellDlg.value = true;
}

async function processRowEditions() {
  appStatus.isProcessing = true;
  if (curModifyType.value === 'create') {
    modification.value.forEach((row) => appStatus.mails.push(row));
    $q.notify({
      type: 'positive',
      icon: 'fa-solid fa-check',
      message: 'Success to add new rows',
    });
    await nextTick();
    appStatus.mailTableRef?.scrollTo(modification.value[modification.value.length - 1].Index - 1, 'end');
    resetConfig();
  } else {
    appStatus.mails = appStatus.mails.filter((mail) => (
      !appStatus.selectedRows.some((selected) => selected.Index === mail.Index)
    ));
    appStatus.mails.forEach((data, index) => { data.Index = index + 1; });
    appStatus.selectedRows.length = 0;
    $q.notify({
      type: 'positive',
      icon: 'fa-solid fa-check',
      message: 'Success to delete selected rows',
    });
  }
  appStatus.isProcessing = false;
}

function viewCellContent(event) {
  if (event.target.matches('.dataCell')) {
    curCellContent.value = event.target.textContent;
    displayViewCellDlg.value = true;
  }
}

function fillEntireCol() {
  const dataList = batchCellNewContent.value.split(/\n/).filter((data) => data !== '');

  modification.value.forEach((_, index) => {
    modification.value[index][curEditCol.value] = dataList[index] || dataList[dataList.length - 1];
  });
  batchCellNewContent.value = '';
  curEditCol.value = null;
}
</script>

<style>
.rowSelectScrollArea .q-scrollarea__content {
  width: 100%;
}
</style>
