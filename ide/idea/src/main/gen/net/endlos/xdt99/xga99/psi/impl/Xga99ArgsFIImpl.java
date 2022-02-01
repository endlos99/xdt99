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

public class Xga99ArgsFIImpl extends ASTWrapperPsiElement implements Xga99ArgsFI {

  public Xga99ArgsFIImpl(@NotNull ASTNode node) {
    super(node);
  }

  public void accept(@NotNull Xga99Visitor visitor) {
    visitor.visitArgsFI(this);
  }

  @Override
  public void accept(@NotNull PsiElementVisitor visitor) {
    if (visitor instanceof Xga99Visitor) accept((Xga99Visitor)visitor);
    else super.accept(visitor);
  }

  @Override
  @NotNull
  public Xga99OpValue getOpValue() {
    return findNotNullChildByClass(Xga99OpValue.class);
  }

}
