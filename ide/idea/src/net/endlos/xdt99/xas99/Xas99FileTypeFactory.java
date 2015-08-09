package net.endlos.xdt99.xas99;

import com.intellij.openapi.fileTypes.FileTypeConsumer;
import com.intellij.openapi.fileTypes.FileTypeFactory;
import org.jetbrains.annotations.NotNull;

public class Xas99FileTypeFactory extends FileTypeFactory{
    @Override
    public void createFileTypes(@NotNull FileTypeConsumer fileTypeConsumer) {
        fileTypeConsumer.consume(Xas99FileType.INSTANCE, "a99");
    }
}
