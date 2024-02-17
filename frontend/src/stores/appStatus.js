import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useAppStatusStore = defineStore('AppStatus', () => {
  const svrUrl = `http://${window.location.host}`;

  const mailFile = ref(null);
  const mails = ref([]);

  const fieldCorrespond = ref({
    uid: null,
    title: null,
    content: null,
  });
  const selectedRows = ref([]);

  const isProcessing = ref(false);
  const displayModifyColDlg = ref(false);
  const displayModifyRowDlg = ref(false);
  const rowModifyType = ref('add');

  return {
    svrUrl,
    mailFile,
    mails,
    fieldCorrespond,
    selectedRows,
    isProcessing,
    displayModifyColDlg,
    displayModifyRowDlg,
    rowModifyType,
  };
});
