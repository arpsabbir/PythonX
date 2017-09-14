from xx import filex
from xx import iox
import os
import filecmp

import shutil
import zipfile


class TranslationFile:
    """主要用要翻译后的处理文件
    打包jar包，
    备份、替换、还原j等
    """

    file_list = [
        'lib/resources_en.jar',
    ]

    def main(self):
        source_dir = r'D:\xx\software\program\android\AndroidStudio'
        "源目录"

        backup_dir = r'D:\workspace\TranslatorX\AndroidStudio\original\2.3.3'
        "备份目录，不可修改，要修于备分"

        work_dir = r'D:\workspace\TranslatorX\AndroidStudio\target\2.3.3'
        "要替换的文件所在的目录"

        action_list = [
            ['退出', exit],
            ['备份文件,%s到%s' % (source_dir, backup_dir), self.copy_dir, source_dir, backup_dir],
            ['恢复文件,%s到%s' % (backup_dir, source_dir), self.copy_dir, backup_dir, source_dir],
            ['复制备份文件到工作目录,%s到%s' % (backup_dir, work_dir), self.copy_dir, backup_dir, work_dir],
            ['打包jar文件,%s到%s' % (work_dir, work_dir), self.jar_file, work_dir, work_dir],
            ['替换源文件,%s到%s' % (work_dir, source_dir), self.copy_dir, work_dir, source_dir],
            ['打包并替换', self.jar_file_and_replace, work_dir, work_dir, source_dir]
        ]
        iox.choose_action(action_list)

    @staticmethod
    def copy_dir(source_dir, target_dir):
        """备份"""
        for file in TranslationFile.file_list:
            source_file = '%s/%s' % (source_dir, file)
            if not os.path.exists(source_file):
                print('文件不存在%s' % source_file)
                continue
            target_file = '%s/%s' % (target_dir, file)
            if os.path.exists(target_file):
                if filecmp.cmp(source_file, target_file):
                    print('文件已相同%s与%s' % (source_file, target_file))
                    continue
            shutil.copyfile(source_file, target_file)
            print('复制文件%s到%s' % (source_file, target_file))
        pass

    @staticmethod
    def jar_file(jar_file_dir, jar_content_dir):
        """
        打包jar文件
        本来也可以直接打包到源目录，但为了可以提供jar包，就打包到工作目录
        """
        for file in TranslationFile.file_list:
            source_file = '%s/%s' % (jar_file_dir, file)
            print('处理%s' % source_file)
            if not os.path.exists(source_file):
                print('文件不存在%s' % source_file)
                continue
            work_jar_file = '%s/%s' % (jar_content_dir, file)
            work_jar_dir = os.path.splitext(work_jar_file)[0]
            with zipfile.ZipFile(source_file, 'a') as zip_file:
                work_file_list = filex.list_file(work_jar_dir)
                print('压缩%d个文件' % len(work_file_list))
                for work_file in work_file_list:
                    # 相对于jar目录，所以替换
                    zip_file.write(work_file, arcname=work_file.replace(work_jar_dir, ''))

    @staticmethod
    def jar_file_and_replace(jar_file_dir, jar_content_dir, target_dir):
        """打包并替换"""
        TranslationFile.jar_file(jar_file_dir, jar_content_dir)
        TranslationFile.copy_dir(jar_file_dir, target_dir)


if __name__ == '__main__':
    TranslationFile().main()
