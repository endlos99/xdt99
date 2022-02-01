// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xga99.psi.impl;

import java.util.List;
import org.jetbrains.annotations.*;
import com.intellij.lang.ASTNode;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiElementVisitor;
import com.intellij.psi.util.PsiTreeUtil;
import static net.endlos.xdt99.xga99.psi.Xga99Types.*;
import com.intellij.extapi.psi.ASTWrapperPsiElement;
import net.endlos.xdt99.xga99.psi.*;

public class Xga99ArgsIXImpl extends ASTWrapperPsiElement implements Xga99ArgsIX {

  public Xga99ArgsIXImpl(@NotNull ASTNode node) {
    super(node);
  }

  public void accept(@NotNull Xga99Visitor visitor) {
    visitor.visitArgsIX(this);
  }

  @Override
  public void accept(@NotNull PsiElementVisitor visitor) {
    if (visitor instanceof Xga99Visitor) accept((Xga99Visitor)visitor);
    else super.accept(visitor);
  }

  @Override
  @Nullable
  public Xga99OpGs getOpGs() {
    return findChildByClass(Xga99OpGs.class);
  }

  @Override
  @Nullable
  public Xga99OpMd getOpMd() {
    return findChildByClass(Xga99OpMd.class);
  }

  @Override
  @Nullable
  public Xga99OpMs getOpMs() {
    return findChildByClass(Xga99OpMs.class);
  }

  @Override
  @Nullable
  public Xga99OpValue getOpValue() {
    return findChildByClass(Xga99OpValue.class);
  }

}
