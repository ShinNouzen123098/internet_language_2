new Vue({
    el: '#vue-league-table',
    data: {
      showTable: true,
      filterText: '',
      teams: [
        { name: 'Зенит-Казань', games: 28, wins: 27, loses: 1, points: 79 },
        { name: 'Динамо Москва', games: 28, wins: 23, loses: 5, points: 64 },
        { name: 'Белогорье', games: 28, wins: 24, loses: 4, points: 64 },
        { name: 'Локомотив', games: 28, wins: 24, loses: 4, points: 63 },
        { name: 'Зенит Санкт-Петербург', games: 28, wins: 22, loses: 6, points: 61 },
        { name: 'Динамо-ЛО', games: 28, wins: 20, loses: 8, points: 48 },
        { name: 'Факел', games: 28, wins: 18, loses: 10, points: 45 },
        { name: 'Урал', games: 28, wins: 16, loses: 12, points: 41 },
        { name: 'Енисей', games: 28, wins: 15, loses: 13, points: 39 },
        { name: 'Газпром-Югра', games: 28, wins: 14, loses: 14, points: 37 }
      ]
    },
    computed: {
      filteredTeams() {
        if (!this.filterText.trim()) return this.teams;
        return this.teams.filter(team =>
          team.name.toLowerCase().includes(this.filterText.trim().toLowerCase())
        );
      }
    },
    methods: {
      toggleTable() {
        this.showTable = !this.showTable;
      }
    }
  });