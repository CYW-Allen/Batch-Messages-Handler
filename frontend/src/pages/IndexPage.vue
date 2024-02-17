<template>
  <q-page :style-fn="tweakPageH" class="q-pa-lg bg-light-blue-1">
    <div class="fit column">
      <div class="col-10 q-pa-sm">
        <div class="fit row">
          <div class="col-8 full-height" style="border: 1px solid blue;">Data field</div>
          <div class="col full-height" style="border: 1px solid green;">Operation field</div>
        </div>
      </div>
      <div class="col-2 q-px-sm">
        <div class="fit" style="border: 1px solid purple;">Request handler field</div>
      </div>
    </div>
  </q-page>
</template>

<script setup>

function tweakPageH(offset) {
  return { height: offset ? `calc(100vh - ${offset}px)` : '100vh' };
}

</script>
