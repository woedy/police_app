from django.contrib import admin

from reports.models import Report, ReportComment, ReportImage, ReportVideo, Officer, UploadReport, UploadReportTag, \
    UploadReportComment, RecordReport, RecordReportComment, RecordReportTag, LiveReport, LiveReportComment

admin.site.register(Report)
admin.site.register(ReportComment)
admin.site.register(ReportImage)
admin.site.register(ReportVideo)
admin.site.register(Officer)


admin.site.register(UploadReport)
admin.site.register(UploadReportTag)
admin.site.register(UploadReportComment)


admin.site.register(RecordReport)
admin.site.register(RecordReportTag)
admin.site.register(RecordReportComment)

admin.site.register(LiveReport)
admin.site.register(LiveReportComment)
