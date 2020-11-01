export const statusMixin = {
  methods: {
    lessonStatus: function (status) {
      if (status !== null) return status
      else { return 'Not Started' }
    }
  }
}
