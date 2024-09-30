<template>

    <div class="p-20 px-52">
      <div class="flex flex-col">
        <div class="flex overflow-hidden rounded-t-md bg-[#1e293b] border p-2">
          <ul class="flex list-none p-0">
            <li v-for="(tab, index) in tabs" :key="index" class="mr-2">
              <button
                  @click="setActiveTab(index)"
                  :class="activeTab === index ? 'bg-red-600' : 'bg-[#636365]'"
                  class="px-4 py-2 cursor-pointer">
                {{ tab.name }}
                <span @click.stop="closeTab(index)" class="ml-2 cursor-pointer">×</span>
              </button>
            </li>
            <li class="ml-auto">
              <button @click="addNewTab" class="px-4 py-2 bg-[#636365] cursor-pointer">+ New Tab</button>
            </li>
          </ul>
        </div>
        <div class="">
          <div v-for="(tab, index) in tabs" :key="index" v-show="activeTab === index" class="text-white">
            <LabTerminal container-id="d8f957f4c796"/>
            <!-- Placeholder for terminal content. Replace with actual terminal logic or iframe -->
          </div>
        </div>
      </div>
    </div>
</template>

<script>
export default {
  data() {
    return {
      tabs: [{ name: "Terminal 1" }],
      activeTab: 0,
    };
  },
  methods: {
    setActiveTab(index) {
      this.activeTab = index;
    },
    addNewTab() {
      this.tabs.push({ name: `Terminal ${this.tabs.length + 1}` });
      this.activeTab = this.tabs.length - 1;
    },
    closeTab(index) {
      this.tabs.splice(index, 1);
      if (this.activeTab >= this.tabs.length) {
        this.activeTab = this.tabs.length - 1;
      }
    },
  },
};
</script>

<style scoped>
/* Tailwind classes replace custom CSS */
</style>
