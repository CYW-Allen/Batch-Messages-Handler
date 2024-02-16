<template>
  <q-page :style-fn="tweakPageH" class="q-pa-lg bg-light-blue-1">
    <div class="fit column">
      <div class="col-10 q-pa-sm">
        <div class="fit row">
        </div>
      </div>
      <div class="col-2 q-px-sm">
      </div>
    </div>
  </q-page>
</template>

<script setup>

function tweakPageH(offset) {
  return { height: offset ? `calc(100vh - ${offset}px)` : '100vh' };
}

</script>
